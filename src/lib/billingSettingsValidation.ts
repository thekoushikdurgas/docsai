/** Client-side validation aligned with Django `admin_ops.views._validate_billing_settings_input`. */

export function validateBillingSettingsInput(input: {
  upiId: string;
  phoneNumber: string;
  email: string;
  qrCodeS3Key?: string | null;
}): string[] {
  const errors: string[] = [];
  const upiId = input.upiId.trim();
  const phoneNumber = input.phoneNumber.trim();
  const email = input.email.trim();
  const qrCodeS3Key = input.qrCodeS3Key?.trim() || null;

  if (!upiId) {
    errors.push("UPI ID is required.");
  } else if (!/^[A-Za-z0-9._-]{2,256}@[A-Za-z]{2,64}$/.test(upiId)) {
    errors.push("UPI ID format is invalid.");
  }

  if (phoneNumber) {
    let normalized = phoneNumber.replace(/\s/g, "").replace(/-/g, "");
    if (normalized.startsWith("+")) normalized = normalized.slice(1);
    if (!/^\d+$/.test(normalized) || normalized.length < 8 || normalized.length > 15) {
      errors.push("Phone number must be 8-15 digits (optional leading +).");
    }
  }

  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    errors.push("Email format is invalid.");
  }

  if (qrCodeS3Key) {
    if (qrCodeS3Key.includes("..") || qrCodeS3Key.startsWith("/") || qrCodeS3Key.endsWith("/")) {
      errors.push("QR key path is invalid.");
    } else if (!qrCodeS3Key.startsWith("photo/")) {
      errors.push("QR key must be under photo/ prefix.");
    }
  }

  return errors;
}
