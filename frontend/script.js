
/* ======================================
   DOM ELEMENTS
====================================== */

const imageInput =
document.getElementById("imageInput");

const preview =
document.getElementById("preview");

const analyzeBtn =
document.getElementById("analyzeBtn");

const predictionText =
document.getElementById("predictionText");

const predictionIcon =
document.getElementById("predictionIcon");

const confidenceValue =
document.getElementById("confidenceValue");

const confidenceBar =
document.getElementById("confidenceBar");

const realProb =
document.getElementById("realProb");

const morphProb =
document.getElementById("morphProb");

const predictionScore =
document.getElementById("predictionScore");


/* ======================================
   IMAGE PREVIEW
====================================== */

imageInput.addEventListener(
    "change",
    (event) => {

        const file =
        event.target.files[0];

        if (!file) return;

        preview.src =
        URL.createObjectURL(file);

        preview.style.display =
        "block";
    }
);


/* ======================================
   CONFIDENCE CHART
====================================== */

let confidenceChart;

function updateConfidenceChart(
    confidence
){

    const ctx =
    document
    .getElementById("confidenceChart")
    .getContext("2d");

    if(confidenceChart){

        confidenceChart.destroy();
    }

    confidenceChart =
    new Chart(ctx, {

        type:"doughnut",

        data:{
            datasets:[
            {
                data:[
                    confidence,
                    100-confidence
                ],

                backgroundColor:[
                    "#22c55e",
                    "#ef4444"
                ],

                borderWidth:0
            }]
        },

        options:{

            responsive:true,

            cutout:"72%",

            plugins:{
                legend:{
                    display:false
                },

                tooltip:{
                    enabled:false
                }
            }
        }
    });
}


/* ======================================
   PROCESSING ANIMATION
====================================== */

async function fakeProcessing(){

    predictionText.innerHTML =
    "Analyzing...";

    predictionIcon.innerHTML =
    "⏳";

    await new Promise(
        r => setTimeout(r,600)
    );
}


/* ======================================
   API CALL
====================================== */

analyzeBtn.addEventListener(
    "click",
    async () => {

        const file =
        imageInput.files[0];

        if(!file){

            alert(
                "Please upload an image."
            );

            return;
        }

        analyzeBtn.disabled = true;

        analyzeBtn.innerHTML =
        "Analyzing...";

        await fakeProcessing();

        try{

            const formData =
            new FormData();

            formData.append(
                "file",
                file
            );

            const response =
            await fetch(
                "https://https://face-morph-detection-model.onrender.com/predict",
                {
                    method:"POST",
                    body:formData
                }
            );

            const data =
            await response.json();

            updateDashboard(data);

        }
        catch(error){

            console.error(error);

            predictionText.innerHTML =
            "Prediction Failed";

            predictionIcon.innerHTML =
            "❌";
        }

        analyzeBtn.disabled = false;

        analyzeBtn.innerHTML =
        "Analyze Again";
    }
);


/* ======================================
   DASHBOARD UPDATE
====================================== */

function updateDashboard(data){

    const label =
    data.label;

    const confidence =
    Number(data.confidence);

    const real =
    Number(data.real_probability);

    const morph =
    Number(data.morph_probability);

    const raw =
    Number(data.raw_prediction);


    /* -------------------------
       RESULT STATUS
    ------------------------- */

    if(label === "REAL"){

        predictionText.innerHTML =
        "REAL DETECTED";

        predictionText.style.color =
        "#16a34a";

        predictionIcon.innerHTML =
        "✅";

        confidenceBar.style.background =
        "#22c55e";
    }

    else{

        predictionText.innerHTML =
        "MORPH DETECTED";

        predictionText.style.color =
        "#ef4444";

        predictionIcon.innerHTML =
        "⚠️";

        confidenceBar.style.background =
        "#ef4444";
    }


    /* -------------------------
       CONFIDENCE
    ------------------------- */

    confidenceValue.innerHTML =
    confidence.toFixed(2) + "%";

    confidenceBar.style.width =
    confidence + "%";


    /* -------------------------
       PROBABILITIES
    ------------------------- */

    realProb.innerHTML =
    real.toFixed(2) + "%";

    morphProb.innerHTML =
    morph.toFixed(2) + "%";


    /* -------------------------
       RAW SCORE
    ------------------------- */

    predictionScore.innerHTML =
    raw.toFixed(6);


    /* -------------------------
       CHART
    ------------------------- */

    updateConfidenceChart(
        confidence
    );
}


/* ======================================
   ACCURACY CHART
====================================== */

const accuracyCtx =
document
.getElementById("accuracyChart")
.getContext("2d");

new Chart(accuracyCtx,{

    type:"line",

    data:{

        labels:[
            "Epoch 1",
            "Epoch 2",
            "Epoch 3",
            "Epoch 4",
            "Epoch 5",
            "Epoch 6"
        ],

        datasets:[

            {

                label:
                "Train Accuracy",

                data:[
                    0.43,
                    0.91,
                    0.94,
                    0.95,
                    0.96,
                    0.97
                ],

                borderColor:
                "#3b82f6",

                backgroundColor:
                "rgba(59,130,246,.15)",

                tension:0.4,

                fill:true
            },

            {

                label:
                "Validation Accuracy",

                data:[
                    0.90,
                    0.90,
                    0.93,
                    0.94,
                    0.95,
                    0.96
                ],

                borderColor:
                "#f97316",

                backgroundColor:
                "rgba(249,115,22,.12)",

                tension:0.4,

                fill:true
            }
        ]
    },

    options:{

        responsive:true,

        maintainAspectRatio:false,

        plugins:{
            legend:{
                display:true
            }
        }
    }
});


/* ======================================
   INITIAL STATE
====================================== */

updateConfidenceChart(0);

