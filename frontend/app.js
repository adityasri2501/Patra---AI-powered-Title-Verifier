async function verifyTitle() {
  const title = document.getElementById("titleInput").value.trim();
  if (!title) {
    alert("Enter a title first");
    return;
  }

  document.getElementById("result").classList.add("hidden");
  document.getElementById("loader").classList.remove("hidden");
  document.getElementById("loader").classList.remove("hidden");
  document.getElementById("loader").classList.add("hidden");


  try {
    const res = await fetch("http://127.0.0.1:5000/verify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title })
    });

    const data = await res.json();
    showResult(data);

  } catch (err) {
    alert("Backend not reachable");
  } finally {
    document.getElementById("loader").classList.add("hidden");
  }
}

function showResult(data) {
  const statusEl = document.getElementById("status");
  statusEl.innerText = data.status;
  statusEl.className = "status-" + data.status;

  document.getElementById("reason").innerText =
    data.reason || "No conflict detected";

  document.getElementById("phonetic").innerText =
    data.scores?.phonetic ?? "-";

  document.getElementById("string").innerText =
    data.scores?.string ?? "-";

  document.getElementById("semantic").innerText =
    data.scores?.semantic ?? "-";

  document.getElementById("matched").innerText =
    data.matched_title || "—";

  document.getElementById("policy").innerText =
    data.policy_code;

  document.getElementById("prob").innerText =
    data.verification_probability;

  document.getElementById("result").classList.remove("hidden");
}

console.log("Backend response:", data);