"""Public legal pages (Terms, Privacy, Refund)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


@dataclass(frozen=True)
class LegalSection:
    anchor: str
    heading: str
    body: str


def _slugify_anchor(text: str) -> str:
    return (
        "".join(ch.lower() if ch.isalnum() else "-" for ch in text).strip("-").replace("--", "-")
    )


def _render(
    request: HttpRequest,
    *,
    page_type: str,
    page_title: str,
    last_updated: str,
    intro: str,
    sections: List[LegalSection],
) -> HttpResponse:
    return render(
        request,
        "legal/page.html",
        {
            "show_authenticated_layout": False,
            "page_type": page_type,
            "page_title": page_title,
            "last_updated": last_updated,
            "intro": intro,
            "sections": sections,
            "toc": [{"anchor": s.anchor, "heading": s.heading} for s in sections],
        },
    )


def terms_view(request: HttpRequest) -> HttpResponse:
    sections = [
        LegalSection(
            anchor="acceptance",
            heading="1. Acceptance of Terms",
            body=(
                "By accessing or using Contact360, you confirm that you have read, understood, and "
                "agree to be bound by these Terms and our Privacy Policy. If you do not agree, do not use the Service."
            ),
        ),
        LegalSection(
            anchor="service",
            heading="2. Description of Service",
            body="Contact360 provides tools for discovering and verifying business contact information and related workflow features. Features may vary by plan and may change over time.",
        ),
        LegalSection(
            anchor="payments",
            heading="3. Subscriptions, Billing & Payments",
            body="Paid plans are billed in advance and may auto-renew unless cancelled. Payments are processed via third-party payment processors (including Razorpay). We do not store full card details on our servers.",
        ),
        LegalSection(
            anchor="cancellation",
            heading="4. Cancellation",
            body="You may cancel your subscription at any time from your account settings. Cancellation stops future renewals; it does not automatically refund amounts already paid except as described in our Refund Policy.",
        ),
        LegalSection(
            anchor="acceptable-use",
            heading="5. Acceptable Use",
            body="You agree not to misuse the Service, including attempting to access accounts without authorization, sending unlawful communications, or violating any applicable laws (including privacy and anti-spam laws).",
        ),
        LegalSection(
            anchor="liability",
            heading="6. Disclaimers & Limitation of Liability",
            body='The Service is provided on an \"as is\" basis. To the maximum extent permitted by law, Contact360 disclaims warranties of any kind and will not be liable for indirect, incidental, special, consequential, or punitive damages.',
        ),
        LegalSection(
            anchor="law",
            heading="7. Disputes & Governing Law",
            body="These Terms are governed by the laws of India. Any disputes will be subject to the exclusive jurisdiction of the courts located in India, unless otherwise required by applicable law.",
        ),
        LegalSection(
            anchor="contact",
            heading="8. Contact",
            body="For questions about these Terms, please contact support via our website or your account support channel.",
        ),
    ]
    return _render(
        request,
        page_type="terms",
        page_title="Terms of Service",
        last_updated="2026-03-18",
        intro="These Terms of Service govern your use of the Contact360 platform (\"Service\"). By accessing or using the Service, you agree to these Terms.",
        sections=sections,
    )


def privacy_view(request: HttpRequest) -> HttpResponse:
    sections = [
        LegalSection(
            anchor="overview",
            heading="1. Overview",
            body="We are committed to protecting your personal data and respecting your privacy. This policy describes what information we collect, how we use it, and the choices available to you.",
        ),
        LegalSection(
            anchor="collect",
            heading="2. Information We Collect",
            body="We may collect information you provide (such as name, email, company), information generated through your use of the Service (such as usage logs), and technical data (such as device, browser, and IP address).",
        ),
        LegalSection(
            anchor="use",
            heading="3. How We Use Your Information",
            body="We use information to provide and improve the Service, process transactions, respond to support requests, maintain security, prevent fraud, and comply with legal obligations.",
        ),
        LegalSection(
            anchor="payments",
            heading="4. Payments and Razorpay",
            body="When you make a purchase, payment processing is handled by third-party payment processors (including Razorpay). We do not store your full card details. Payment processors may collect and process payment information according to their policies.",
        ),
        LegalSection(
            anchor="cookies",
            heading="5. Cookies",
            body="We use cookies and similar technologies to enable core functionality (such as authentication), remember preferences, and understand how the Service is used. You can control cookies through your browser settings.",
        ),
        LegalSection(
            anchor="retention",
            heading="6. Data Retention",
            body="We retain personal information for as long as necessary to provide the Service and for legitimate business purposes such as compliance, dispute resolution, and enforcement of our agreements.",
        ),
        LegalSection(
            anchor="rights",
            heading="7. Your Rights",
            body="Depending on your location, you may have rights to access, correct, delete, or restrict certain processing of your personal data. To exercise these rights, contact support through our website or your account support channel.",
        ),
        LegalSection(
            anchor="security",
            heading="8. Security",
            body="We implement reasonable safeguards to protect your information. However, no system is completely secure and we cannot guarantee absolute security.",
        ),
        LegalSection(
            anchor="contact",
            heading="9. Contact",
            body="For privacy questions or requests, please contact support via our website or your account support channel.",
        ),
    ]
    return _render(
        request,
        page_type="privacy",
        page_title="Privacy Policy",
        last_updated="2026-03-18",
        intro="This Privacy Policy explains how Contact360 collects, uses, and protects your data when you use our website and services.",
        sections=sections,
    )


def refund_view(request: HttpRequest) -> HttpResponse:
    sections = [
        LegalSection(
            anchor="overview",
            heading="1. Overview",
            body="If you believe you were charged incorrectly or are eligible for a refund, you can request one using the process below. This policy applies to purchases made directly through Contact360 checkout.",
        ),
        LegalSection(
            anchor="eligible",
            heading="2. Eligible Refunds",
            body="Refunds may be considered for duplicate charges, failed provisioning after a successful charge, or a material service outage preventing core functionality during the refund window. Eligibility is determined on a case-by-case basis.",
        ),
        LegalSection(
            anchor="nonrefundable",
            heading="3. Non-Refundable Items",
            body="Unless required by applicable law, we typically do not refund usage-based credits that have been consumed, services already delivered, or charges older than the refund window.",
        ),
        LegalSection(
            anchor="window",
            heading="4. Refund Window",
            body="Refund requests must be submitted within 7 calendar days of the original purchase date, unless a longer period is required by applicable law.",
        ),
        LegalSection(
            anchor="request",
            heading="5. How to Request a Refund",
            body="Contact support with your account email, invoice/transaction reference, purchase date, and a brief description of the issue. We may request additional information to verify the purchase.",
        ),
        LegalSection(
            anchor="processing",
            heading="6. Processing Time",
            body="If approved, refunds are processed back to the original payment method via our payment partners (including Razorpay). Processing time typically takes 5–7 business days depending on your bank/payment method.",
        ),
        LegalSection(
            anchor="contact",
            heading="7. Contact",
            body="For refund requests and questions, please contact support via our website or your account support channel.",
        ),
    ]
    return _render(
        request,
        page_type="refund",
        page_title="Refund Policy",
        last_updated="2026-03-18",
        intro="This Refund Policy explains when you may be eligible for a refund and how to request one. Refunds are issued back to the original payment method via our payment partners (including Razorpay).",
        sections=sections,
    )

