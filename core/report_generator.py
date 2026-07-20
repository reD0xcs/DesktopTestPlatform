import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors


class ReportGenerator:

    def __init__(self):
        self.output_dir = os.path.join(os.getcwd(), "reports")
        os.makedirs(self.output_dir, exist_ok=True)

    # ==================================================
    # PUBLIC
    # ==================================================

    def generate(self, product, results, metadata, measurements):

        test_id = metadata["test_id"]
        report_path = os.path.join(self.output_dir, f"{test_id}.pdf")

        c = canvas.Canvas(report_path, pagesize=A4)
        width, height = A4

        y = height - 30 * mm

        # ==================================================
        # HEADER
        # ==================================================

        c.setFont("Helvetica-Bold", 18)
        c.drawString(20 * mm, y, "TEST REPORT")
        y -= 10 * mm

        c.setFont("Helvetica", 12)
        c.drawString(20 * mm, y, f"Product: {product.name}")
        y -= 6 * mm

        c.drawString(20 * mm, y, f"Version: {product.version}")
        y -= 6 * mm

        c.drawString(20 * mm, y, f"Test ID: {metadata['test_id']}")
        y -= 6 * mm

        c.drawString(20 * mm, y, f"SSH Hash: {metadata['ssh_hash']}")
        y -= 6 * mm

        # QR code
        c.drawImage(
            metadata["qr_path"],
            width - 50 * mm,
            height - 50 * mm,
            40 * mm,
            40 * mm
        )

        y -= 10 * mm
        self._draw_separator(c, y, width)
        y -= 8 * mm

        # ==================================================
        # TEST SUMMARY
        # ==================================================

        total_steps = len(results)
        passed = sum(1 for r in results if r.success)
        failed = sum(1 for r in results if not r.success)
        first_fail = next((r.action_id for r in results if not r.success), "None")

        c.setFont("Helvetica-Bold", 14)
        c.drawString(20 * mm, y, "Test Summary")
        y -= 8 * mm

        c.setFont("Helvetica", 12)
        c.drawString(20 * mm, y, f"Total steps: {total_steps}")
        y -= 6 * mm
        c.drawString(20 * mm, y, f"Passed: {passed}")
        y -= 6 * mm
        c.drawString(20 * mm, y, f"Failed: {failed}")
        y -= 6 * mm
        c.drawString(20 * mm, y, f"First failure: {first_fail}")
        y -= 6 * mm
        c.drawString(20 * mm, y, f"Duration: {metadata.get('duration', 0):.2f} s")
        y -= 10 * mm

        self._draw_separator(c, y, width)
        y -= 8 * mm

        # ==================================================
        # METADATA
        # ==================================================

        c.setFont("Helvetica-Bold", 14)
        c.drawString(20 * mm, y, "Metadata")
        y -= 8 * mm

        c.setFont("Helvetica", 12)
        for key in ["software_version", "hardware_version", "procedure_id",
                    "batch_number", "serial_number"]:
            value = metadata.get(key, "")
            c.drawString(20 * mm, y, f"{key.replace('_', ' ').title()}: {value}")
            y -= 6 * mm

        y -= 10 * mm
        self._draw_separator(c, y, width)
        y -= 8 * mm

        # ==================================================
        # RESULTS TABLE (INDUSTRIAL)
        # ==================================================

        c.setFont("Helvetica-Bold", 14)
        c.drawString(20 * mm, y, "Test Results")
        y -= 8 * mm

        # Header
        c.setFont("Helvetica-Bold", 12)
        c.drawString(20 * mm, y, "Action")
        c.drawString(90 * mm, y, "Status")
        c.drawString(130 * mm, y, "Message")
        y -= 6 * mm

        c.setFont("Helvetica", 12)

        for result in results:
            # background color per row
            if result.success:
                c.setFillColor(colors.green)
            else:
                c.setFillColor(colors.red)

            c.rect(18 * mm, y - 2, width - 36 * mm, 14, fill=1, stroke=0)
            c.setFillColor(colors.white)

            c.drawString(20 * mm, y, result.action_id[:40])
            c.drawString(90 * mm, y, "PASS" if result.success else "FAIL")
            c.drawString(130 * mm, y, result.message[:40])
            y -= 8 * mm

            c.setFillColor(colors.black)

            if y < 30 * mm:
                c.showPage()
                y = height - 20 * mm

        y -= 10 * mm
        self._draw_separator(c, y, width)
        y -= 8 * mm

        # ==================================================
        # MEASUREMENTS TABLE (INDUSTRIAL)
        # ==================================================

        c.setFont("Helvetica-Bold", 14)
        c.drawString(20 * mm, y, "Measurements")
        y -= 8 * mm

        c.setFont("Helvetica-Bold", 12)
        c.drawString(20 * mm, y, "Time")
        c.drawString(60 * mm, y, "Voltage")
        c.drawString(100 * mm, y, "Current")
        y -= 6 * mm

        c.setFont("Helvetica", 12)

        for (t, v), (_, crr) in zip(measurements["voltage"], measurements["current"]):
            c.drawString(20 * mm, y, f"{t:.2f}")
            c.drawString(60 * mm, y, f"{v:.2f} V")
            c.drawString(100 * mm, y, f"{crr:.2f} A")
            y -= 6 * mm

            if y < 30 * mm:
                c.showPage()
                y = height - 20 * mm

        y -= 10 * mm
        self._draw_separator(c, y, width)
        y -= 8 * mm

        # ==================================================
        # EXECUTION LOG (EXTINS)
        # ==================================================

        c.setFont("Helvetica-Bold", 14)
        c.drawString(20 * mm, y, "Execution Log")
        y -= 8 * mm

        c.setFont("Helvetica", 12)

        for line in metadata["logs"]:
            # highlight FAIL
            if "FAILED at step" in line or "False" in line:
                c.setFillColor(colors.red)
            else:
                c.setFillColor(colors.black)

            c.drawString(20 * mm, y, line[:100])
            y -= 6 * mm

            c.setFillColor(colors.black)

            if y < 30 * mm:
                c.showPage()
                y = height - 20 * mm

        c.save()
        return report_path

    # ==================================================
    # HELPERS
    # ==================================================

    def _draw_separator(self, c, y, width):
        c.setStrokeColor(colors.grey)
        c.setLineWidth(0.5)
        c.line(20 * mm, y, width - 20 * mm, y)
        c.setStrokeColor(colors.black)
