console.log("FULL PIPELINE ACTIVE 🚀");

window.onload = () => {

  let selectedFile = null;

  const uploadZone = document.getElementById("uploadZone");
  const fileInput = document.getElementById("fileInput");
  const analyzeBtn = document.getElementById("analyzeBtn");

  const resultLabel = document.getElementById("resultLabel");
  const confidenceValue = document.getElementById("confidenceValue");
  const progressBar = document.getElementById("progressBarFill");

  const realProb = document.getElementById("realProb");
  const morphProb = document.getElementById("morphProb");
  const insightText = document.getElementById("insightText");
  const steps = document.querySelectorAll(".step-item")

  
  // ==========================
  // UPLOAD
  // ==========================
  uploadZone.onclick = () => fileInput.click();

  fileInput.onchange = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    selectedFile = file;

    const reader = new FileReader();
    reader.onload = (ev) => {
      uploadZone.innerHTML = `
        <img src="${ev.target.result}" 
        style="width:100%;height:100%;object-fit:cover;border-radius:12px;" />
      `;
    };
    reader.readAsDataURL(file);

    analyzeBtn.disabled = false;
  };

  // ==========================
  // ANALYZE
  // ==========================
  analyzeBtn.onclick = async () => {
  async function animateSteps() {
  for (let i = 0; i < steps.length; i++) {
    steps[i].classList.add("active");
    await new Promise(res => setTimeout(res, 400));
  }
    }
    await animateSteps();
    if (!selectedFile) {
      alert("Upload image first");
      return;
    }

    analyzeBtn.innerText = "Analyzing...";
    analyzeBtn.disabled = true;

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const res = await fetch("https://face-morph-detection-model.onrender.com/predict", {
        method: "POST",
        body: formData
      });

      const data = await res.json();
      console.log("API RESPONSE:", data);

      updateUI(data);

    } catch (err) {
      console.error(err);
      alert("Backend error");
    }

    analyzeBtn.innerText = "Analyze Again";
    analyzeBtn.disabled = false;
  };

  // ==========================
  // UPDATE UI
  // ==========================
  function updateUI(data) {

    const morph = data.morph_prob ?? data.confidence;
    const real = data.real_prob ?? (1 - morph);

    let mainVal, color;

    if (data.prediction === "Morph") {
      resultLabel.innerText = "MORPH DETECTED ❌";
      mainVal = morph;
      color = "#ef4444";
    } else {
      resultLabel.innerText = "REAL FACE ✅";
      mainVal = real;
      color = "#22c55e";
    }

    // CONFIDENCE
    animateConfidence(mainVal * 100);

    // BAR
    progressBar.style.width = (mainVal * 100) + "%";
    progressBar.style.background = color;

    // PROBABILITIES
    realProb.innerText = `Real: ${(real * 100).toFixed(2)}%`;
    morphProb.innerText = `Morph: ${(morph * 100).toFixed(2)}%`;

    // INSIGHT
    insightText.innerText =
      data.prediction === "Morph"
        ? "⚠️ Strong morphing patterns detected."
        : "✅ Image appears authentic with no manipulation.";
  }

  // ==========================
  // ANIMATION
  // ==========================
  function animateConfidence(target) {
    let current = 0;

    const interval = setInterval(() => {
      current += target / 30;

      if (current >= target) {
        current = target;
        clearInterval(interval);
      }

      confidenceValue.innerText = current.toFixed(1) + "%";
    }, 25);
  }
  
};
function loadAccuracyChart() {

  const canvas = document.getElementById("accuracyChart");
  if (!canvas) return;

  const ctx = canvas.getContext("2d");

  // 🔥 GRADIENTS
  const gradientBlue = ctx.createLinearGradient(0, 0, 0, 300);
  gradientBlue.addColorStop(0, "rgba(59, 130, 246, 0.4)");
  gradientBlue.addColorStop(1, "rgba(59, 130, 246, 0)");

  const gradientOrange = ctx.createLinearGradient(0, 0, 0, 300);
  gradientOrange.addColorStop(0, "rgba(249, 115, 22, 0.4)");
  gradientOrange.addColorStop(1, "rgba(249, 115, 22, 0)");

  new Chart(ctx, {
    type: "line",
    data: {
      labels: ["Epoch 1", "Epoch 2", "Epoch 3", "Epoch 4", "Epoch 5", "Epoch 6"],
      datasets: [
        {
          label: "Train Accuracy",
          data: [0.43, 0.91, 0.94, 0.95, 0.955, 0.96],
          borderColor: "#3b82f6",
          backgroundColor: gradientBlue,
          fill: true,
          tension: 0.4,
          borderWidth: 3,
          pointRadius: 4,
          pointHoverRadius: 6
        },
        {
          label: "Validation Accuracy",
          data: [0.92, 0.92, 0.935, 0.95, 0.96, 0.965],
          borderColor: "#f97316",
          backgroundColor: gradientOrange,
          fill: true,
          tension: 0.4,
          borderWidth: 3,
          pointRadius: 4,
          pointHoverRadius: 6
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,

      animation: {
        duration: 1500,
        easing: "easeOutQuart"
      },

      plugins: {
        legend: {
          labels: {
            color: "#374151",
            font: {
              size: 12,
              weight: "600"
            }
          }
        }
      },

      scales: {
        x: {
          ticks: {
            color: "#6B7280"
          },
          grid: {
            color: "rgba(0,0,0,0.05)"
          }
        },
        y: {
          ticks: {
            color: "#6B7280"
          },
          grid: {
            color: "rgba(0,0,0,0.05)"
          }
        }
      }
    }
  });

  console.log("🔥 Premium Chart Loaded");
}