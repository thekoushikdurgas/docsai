<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# तो यहाँ आपकी अगली स्टेप साफ़ है: आप Contact360 में फोन नंबर सर्चिंग और वैलिडेशन जोड़ रहे हैं।

इसके लिए, आप पहले अपने डेटाबेस से कोशिश करेंगे और फिर किसी एक्सटर्नल API (जैसे कोई फोन
डेटा प्रोवाइडर) की मदद लेंगे। साथ ही, फोन नंबर वैलिडेशन (जैसे इंटरनेशनल फॉर्मेट चेक, एक्टिव नंबर
चेक) भी जरूरी होगा। जो जॉब आप बनाएंगे, उसमें यूजर CSV देंगे, जिनमें नाम, एड्रेस होंगेहों गेऔर आपकी
जॉब उसमें फोन नंबर ढूंढ कर जोड़ देगी। दूसरी जॉब उन नंबरों की वैलिडिटी चेक कर के एक अलग CSV
देगी। बस ध्यान रखें कि API कॉल्स थ्रॉटलिंग के हिसाब से हों और रिजल्ट्स की एरर हैंडलिंग अच्छी तरह
हो।

बिल्कुल सही समझा आपने! यह email pipeline का exact parallel है — बस domain की जगह address/name से phone number deduce करना है। यहाँ पूरा modular architecture है।

***

## Phone Enrichment + Validation Pipeline

Contact360 में phone pipeline भी email pipeline जैसी same dual-job structure follow करेगी — **Enrichment Job** और **Validation Job**, दोनों independent और swappable। [^1]

***

## Job 1 — Phone Enrichment Service

CSV input में `firstName`, `lastName`, `company`, `address` होगा → output में phone number + confidence score।

### Lookup priority chain

```
Input: { firstName: "Rahul", lastName: "Sharma", company: "Mahindra", city: "Mumbai" }

Step 1: Internal DB Cache
  → Check PostgreSQL: contacts table mein same name+company ka record hai?
  → Hit → return cached phone, skip API call (cost zero)

Step 2: CRM Deduplication Check
  → Existing contacts mein fuzzy match (Levenshtein distance < 2)
  → Match found → link and return

Step 3: External API Lookup
  → Apollo.io / Clearbit / People Data Labs
  → Input: name + company + location
  → Output: phone numbers with type (mobile/office/direct)

Step 4: LinkedIn Enrichment (via integration-service)
  → PhantomBuster / Proxycurl adapter
  → Company page se phone extract

Step 5: Fallback
  → Return { status: "not_found", suggestions: [] }
```


### Enrichment result schema

```typescript
interface PhoneEnrichmentResult {
  phone:        string;          // E.164 format: +917891234567
  type:         "mobile" | "office" | "direct" | "unknown";
  confidence:   number;          // 0.0 → 1.0
  source:       "cache" | "apollo" | "clearbit" | "pdl" | "linkedin";
  countryCode:  string;          // "IN", "US", "GB"
  carrier?:     string;          // "Airtel", "Jio", "Vodafone"
  validated:    boolean;
}
```


***

## Job 2 — Phone Validation Service

Validation एक separate service है क्योंकि यह computationally heavy है और external API rate limits से bound है। [^1]

### Validation pipeline (per number)

```
Input: +917891234567

Step 1: FORMAT / SYNTAX CHECK
  → libphonenumber (Google's library) से parse
  → E.164 format enforce: +[country_code][number]
  → Invalid formats reject: "91-789-123-4567", "07891234567"
  → Normalize: "7891234567" + country hint "IN" → "+917891234567"

Step 2: COUNTRY + CARRIER DETECTION
  → Number range analysis: IN mobile (7,8,9 से शुरू होने वाले)
  → Carrier identification: Jio (6,7), Airtel (8,9), BSNL (94,95)
  → Line type: mobile / landline / toll-free / premium / VoIP

Step 3: ACTIVE NUMBER CHECK (External API)
  → Twilio Lookup API / NumVerify / Telnyx
  → HLR (Home Location Register) lookup: SIM active है?
  → Returns: carrier, line_type, validity

Step 4: DND (Do Not Disturb) CHECK — India specific
  → TRAI DND Registry check (important for marketing use case)
  → Flag: dnd_registered: true/false

Step 5: RISK SCORING
  → VoIP numbers = risky for outreach
  → Disposable virtual numbers = block
  → Recently ported numbers = flag

Output: { status, formatted, carrier, lineType, active, dndRegistered, riskScore }
```


### Validation result schema

```typescript
interface PhoneValidationResult {
  input:          string;           // original input
  formatted:      string;           // +917891234567 (E.164)
  status:         "valid" | "invalid" | "risky" | "unknown";
  reason?:        string;           // "invalid_country_code" | "not_assigned" | "voip" | ...
  countryCode:    string;           // "IN"
  countryName:    string;           // "India"
  carrier:        string | null;    // "Jio"
  lineType:       "mobile" | "landline" | "voip" | "toll_free" | "premium";
  active:         boolean | null;   // HLR lookup result
  dndRegistered:  boolean;          // India TRAI DND
  riskScore:      number;           // 0–100
  checkedAt:      Date;
}
```


***

## Throttling Strategy — API Calls

Phone API calls email से zyada expensive हैं — इसलिए rate limiting पर extra care चाहिए। [^1]

```typescript
// services/phone-service/src/throttle/rate-limiter.ts

const RATE_LIMITS = {
  twilio:   { rpm: 100,  daily: 10_000 },   // per org
  numverify:{ rpm: 50,   daily:  5_000 },
  apollo:   { rpm: 200,  daily: 50_000 },
  pdl:      { rpm: 300,  daily: 100_000 },
};

// Redis token bucket per API per org
async function acquireToken(api: string, orgId: string): Promise<boolean> {
  const key = `ratelimit:${api}:${orgId}`;
  const current = await redis.incr(key);
  if (current === 1) await redis.expire(key, 60);   // 1 minute window
  return current <= RATE_LIMITS[api].rpm;
}
```


### Worker throttling architecture

```
Job Queue (BullMQ/SQS)
  ↓
Phone Worker pulls batch of 100 rows
  ↓
For each row:
  ├── Check Redis token bucket
  ├── Token available → call API immediately
  ├── Token exhausted → add to RETRY queue (delay: 60s)
  └── Daily quota hit → PAUSE worker, alert admin
  ↓
Results written to PostgreSQL
  ↓
Progress event → WebSocket → Frontend
```


***

## Job Architecture (Both Jobs Combined)

```
User uploads CSV (names, addresses)
        ↓
  S3 Presigned PUT URL
        ↓
  Lambda: validate CSV schema
        ↓
  Kafka: phone.enrichment.requested
        ↓
┌─────────────────────────────────────────────────────┐
│              ENRICHMENT WORKER                       │
│                                                      │
│  Row 1: Rahul Sharma, Mahindra, Mumbai               │
│    → DB cache miss                                   │
│    → Apollo API → +917891234567 (confidence: 0.87)   │
│    → Write to PostgreSQL                             │
│    → Publish: phone.enrichment.completed             │
│                                                      │
│  Row 2: bad data → error flagged, job continues      │
└─────────────────────────────────────────────────────┘
        ↓
  Enrichment CSV ready → S3
        ↓
  User triggers Validation Job (or auto-triggered)
        ↓
┌─────────────────────────────────────────────────────┐
│              VALIDATION WORKER                       │
│                                                      │
│  +917891234567 → libphonenumber ✓                    │
│               → Twilio HLR → active: true            │
│               → DND check → false                    │
│               → status: "valid", score: 94           │
│                                                      │
│  +1800XXXXXXX → toll_free → risky for outreach       │
└─────────────────────────────────────────────────────┘
        ↓
  Validation CSV → S3
        ↓
  User notified via notification-service
```


***

## Output CSV Format

### Enrichment output

```csv
firstName,lastName,company,city,phone,phoneType,confidence,source,validated
Rahul,Sharma,Mahindra,Mumbai,+917891234567,mobile,0.87,apollo,false
Priya,Verma,Infosys,Bengaluru,+918901234567,direct,0.91,cache,true
Amit,Kumar,Tata,Delhi,,,,not_found,false
```


### Validation output

```csv
phone,status,formatted,country,carrier,lineType,active,dndRegistered,riskScore,reason
+917891234567,valid,+917891234567,IN,Jio,mobile,true,false,94,
+911234567890,invalid,,,,,false,,0,invalid_number_range
+918800000000,risky,+918800000000,IN,,voip,true,false,35,voip_number
```


***

## Error Handling — Phone-Specific Edge Cases

| Error | Cause | Handling |
| :-- | :-- | :-- |
| `invalid_country_code` | +999 जैसा non-existent code | Reject, flag row |
| `number_too_short` | 7 digits से कम | Reject, suggest correction |
| `ambiguous_format` | `07891234567` without country hint | Try to normalize with org's default country |
| `hlr_timeout` | Carrier HLR server response नहीं आई | Mark `unknown`, retry once |
| `voip_detected` | Virtual/internet number | Flag as `risky`, don't block |
| `dnd_registered` | TRAI DND में registered | Flag, marketing team को alert |
| `api_quota_exceeded` | Daily limit hit | Pause worker, resume next day, notify admin |
| `invalid_name_input` | Blank/null name in CSV | Skip row, count in error summary |
| `no_match_found` | Name+company से कोई phone नहीं मिला | `not_found` status, include in error report |


***

## Modular Adapter Design

Email pipeline की तरह, phone pipeline में भी हर external provider एक swappable adapter है: [^1]

```
phone-enrichment-service/
  ├── adapters/
  │     ├── apollo.adapter.ts        ← name+company → phone
  │     ├── clearbit.adapter.ts
  │     └── people-data-labs.adapter.ts
  ├── validators/
  │     ├── libphonenumber.validator.ts   ← format + country
  │     ├── twilio-hlr.validator.ts       ← active check
  │     ├── numverify.validator.ts
  │     └── dnd-india.validator.ts        ← TRAI DND check
  └── workers/
        ├── enrichment.worker.ts
        └── validation.worker.ts

interface PhoneEnrichmentAdapter {
  findPhone(name: string, company: string, location?: string): Promise<PhoneEnrichmentResult[]>;
}

interface PhoneValidationAdapter {
  validate(phone: string): Promise<PhoneValidationResult>;
}
```


***

## India-Specific Considerations

Contact360 का primary market India है तो कुछ extra checks जरूरी हैं: [^2]

- **TRAI DND Registry** — Marketing calls/SMS के लिए mandatory compliance। DND registered numbers को outreach से automatically exclude करें।
- **E.164 normalization** — Indian numbers often आते हैं as `9XXXXXXXXX`, `+91-9X-XXXX-XXXX`, या `0-9XXXXXXXX` — सब को `+91XXXXXXXXXX` में normalize करें
- **Jio number detection** — 6xxxxxxxxx और 7xxxxxxxxx ranges Jio-specific हैं — useful for carrier-based segmentation
- **Landline format** — `+91-22-XXXXXXXX` (Mumbai STD) जैसे formats को properly parse करें with libphonenumber's `IN` locale

***

पूरा pipeline email enrichment के साथ seamlessly काम करता है — ek hi CSV job में email और phone दोनों एक साथ enrich कर सकते हैं, parallel workers से, without one blocking the other. [^1]

अगला step क्या explore करना है — **libphonenumber integration code**, **Twilio HLR adapter implementation**, या **combined email+phone enrichment job** जो एक ही CSV में दोनों जोड़ दे?

<div align="center">⁂</div>

[^1]: deep-research-report-1.md

[^2]: Pasted-text.txt

