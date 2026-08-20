const FGA_ORIGIN = "https://fga-demo-5wvarmkeaq-du.a.run.app";

const CASES = Object.freeze({
  "bottube-mobile": "https://bottube.ai/",
  "block-explorer": "https://50.28.86.131/explorer",
});

export const config = {
  maxDuration: 300,
};

export default async function handler(req, res) {
  res.setHeader("Cache-Control", "no-store");

  if (req.method !== "GET") {
    res.setHeader("Allow", "GET");
    return res.status(405).json({ error: "GET only" });
  }

  const caseName = String(req.query.case || "");
  const target = CASES[caseName];
  if (!target) {
    return res.status(404).json({
      error: "unknown case",
      allowedCases: Object.keys(CASES),
    });
  }

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 290_000);

  try {
    const auditResponse = await fetch(`${FGA_ORIGIN}/api/audit`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "user-agent": "routezero-fga-bounty-relay/1.0",
      },
      body: JSON.stringify({ url: target }),
      signal: controller.signal,
    });

    const auditText = await auditResponse.text();
    let audit;
    try {
      audit = JSON.parse(auditText);
    } catch {
      audit = { raw: auditText.slice(0, 20_000) };
    }

    if (!auditResponse.ok) {
      return res.status(auditResponse.status).json({
        case: caseName,
        target,
        upstreamStatus: auditResponse.status,
        audit,
      });
    }

    let reportHtml = null;
    let reportStatus = null;
    if (audit && audit.runId) {
      const reportResponse = await fetch(
        `${FGA_ORIGIN}/reports/${encodeURIComponent(audit.runId)}/report.html`,
        { signal: controller.signal },
      );
      reportStatus = reportResponse.status;
      if (reportResponse.ok) {
        reportHtml = (await reportResponse.text()).slice(0, 750_000);
      }
    }

    return res.status(200).json({
      case: caseName,
      target,
      audit,
      reportStatus,
      reportHtml,
      claimBoundary:
        "Relay transport only. FGA results remain inferred candidates requiring human confirmation.",
    });
  } catch (error) {
    const timedOut = controller.signal.aborted;
    return res.status(timedOut ? 504 : 500).json({
      case: caseName,
      target,
      error: timedOut ? "relay timeout" : String(error?.message || error),
    });
  } finally {
    clearTimeout(timer);
  }
}
