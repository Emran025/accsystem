"""Regression tests for consistency between canonical architecture records."""
from __future__ import annotations

import unittest
from pathlib import Path


TEST_DIR = Path(__file__).resolve().parent
ARCH_DIR = TEST_DIR.parents[1]
CONNECTOR_PATH = ARCH_DIR / "c2-containers/accore/CNT-ACR-CONNECTOR.md"
FINANCE_PATH = ARCH_DIR / "c2-containers/accore/CNT-ACR-FINANCE.md"
ADR019_PATH = ARCH_DIR / "decisions/ADR-019.md"
ADR015_PATH = ARCH_DIR / "decisions/ADR-015.md"
DEPLOYMENT_VIEW_PATH = ARCH_DIR / "supporting-views/deployment-view.md"
SYS_ACCORE_PATH = ARCH_DIR / "c1-context/systems/SYS-ACCORE.md"


def table_row(markdown: str, aspect: str) -> tuple[str, str, str]:
    prefix = f"| {aspect} |"
    for line in markdown.splitlines():
        if line.startswith(prefix):
            cells = tuple(cell.strip() for cell in line.strip("|").split("|"))
            if len(cells) == 3:
                return cells
    raise AssertionError(f"Missing {aspect!r} table row")


class ArchitectureSourceConsistencyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.connector = CONNECTOR_PATH.read_text(encoding="utf-8")
        cls.finance = FINANCE_PATH.read_text(encoding="utf-8")
        cls.adr019 = ADR019_PATH.read_text(encoding="utf-8")
        cls.adr015 = ADR015_PATH.read_text(encoding="utf-8")
        cls.deployment_view = DEPLOYMENT_VIEW_PATH.read_text(encoding="utf-8")
        cls.sys_accore = SYS_ACCORE_PATH.read_text(encoding="utf-8")

    def test_adr015_connectivity_choices_are_proposed_and_preserve_all_modes(self):
        rows = {
            aspect: table_row(self.connector, aspect)
            for aspect in ("Transport", "Authentication", "Connectivity model")
        }
        for aspect, row in rows.items():
            with self.subTest(aspect=aspect):
                self.assertIn("PROPOSED (ADR-015)", row[1])
                self.assertNotIn("CONFIRMED", row[1])

        transport = rows["Transport"][2]
        authentication = rows["Authentication"][2]
        connectivity = rows["Connectivity model"][2]
        self.assertIn("HTTPS/TLS", transport)
        self.assertIn("OAuth 2.0 Client Credentials", authentication)
        self.assertIn("mTLS", authentication)
        self.assertIn("outbound-initiated", connectivity)
        for alternative in ("polling", "long-polling", "persistent channel", "protected inbound"):
            with self.subTest(alternative=alternative):
                self.assertIn(alternative.lower(), connectivity.lower())
        self.assertIn("optional", connectivity)
        self.assertIn("approval-gated", connectivity)
        self.assertIn("logical message direction", connectivity)
        self.assertIn("subject to security/owner onboarding approval", self.connector)
        security = self.connector.split("## 7. Security", 1)[1].split("## 8.", 1)[0]
        self.assertNotIn("CONFIRMED (idea.md §4.3): TLS", security)

        self.assertIn("PROPOSED ARCHITECTURAL BASELINE", self.adr015)
        self.assertIn(
            "outbound-initiated authenticated connectivity with polling/long-polling or a persistent channel",
            self.adr015,
        )
        self.assertIn("Protected inbound connectivity is optional", self.adr015)
        self.assertIn(
            "policy-controlled adapter supporting OAuth 2.0 Client Credentials and mTLS",
            self.adr015,
        )
        self.assertIn("No named approval is asserted", self.adr015)

        self.assertIn("Connectivity baseline (PROPOSED under ADR-015)", self.deployment_view)
        self.assertIn(
            "polling, long-polling or a persistent channel may be selected by operations",
            self.deployment_view,
        )
        self.assertIn("protected inbound remains optional", self.deployment_view)
        self.assertIn("logical interaction arrows do not choose network initiation", self.deployment_view)

        self.assertIn("primary integration posture is outbound-initiated", self.sys_accore)
        self.assertIn("Where an approved deployment selects protected inbound", self.sys_accore)
        self.assertIn(
            "Authentication and certificate/token identity binding are policy-selected under ADR-015",
            self.sys_accore,
        )
        self.assertIn("authentication mode PROPOSED/approval-required", self.sys_accore)

        connectivity_sources = {
            "ADR-015": self.adr015,
            "deployment-view": self.deployment_view,
            "SYS-ACCORE": self.sys_accore,
        }
        for source_name, source in connectivity_sources.items():
            for alternative in ("polling", "long-polling", "persistent channel", "protected inbound"):
                with self.subTest(source=source_name, alternative=alternative):
                    self.assertIn(alternative.lower(), source.lower())

        authentication_sources = {
            "ADR-015": self.adr015,
            "SYS-ACCORE": self.sys_accore,
        }
        for source_name, source in authentication_sources.items():
            with self.subTest(source=source_name, concern="authentication alternatives"):
                self.assertIn("OAuth 2.0 Client Credentials", source)
                self.assertIn("mTLS", source)

    def test_finance_receives_order_events_without_defining_universal_posting_trigger(self):
        relationship = next(
            line for line in self.finance.splitlines()
            if line.startswith("| CNT-ACR-SALES |")
        )
        self.assertIn("Receives sales/order events as inputs", relationship)
        self.assertIn("institution's approved local accounting policy (ADR-019)", relationship)
        self.assertIn("not by this event relationship or a universal OrderConfirmed rule", relationship)
        self.assertNotIn("Sales events trigger financial entries", relationship)
        self.assertIn("does **not** assert a universal financial journal posting obligation", self.adr019)
        self.assertIn("OrderConfirmed receipt", self.adr019)
        self.assertIn("later event", self.adr019)
        self.assertIn("PROPOSED/approval-required", self.adr019)


if __name__ == "__main__":
    unittest.main()
