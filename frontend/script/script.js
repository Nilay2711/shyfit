$(document).ready(function () {

  // -------------------------------
  // DOM Elements
  // -------------------------------
  const $searchInput = $("#searchInput");
  const $searchBtn = $("#searchBtn");

  const $workoutContainer = $("#workoutContainer");
  const $exerciseContainer = $("#exerciseContainer");
  const $knowledgeContainer = $("#knowledgeContainer");

  const $chatBtn = $("#chatToggleBtn");
  const $chatPanel = $("#chatPanel");
  const $closeBtn = $("#closeChatBtn");

  const $chatInput = $("#chatInput");
  const $sendBtn = $("#sendBtn");
  const $chatMessages = $("#chatMessages");

  // -------------------------------
  // Initial Focus
  // -------------------------------
  $searchInput.focus();

  // -------------------------------
  // Chat Toggle
  // -------------------------------
  $chatBtn.on("click", function () {
    $chatPanel.removeClass("translate-x-full").addClass("translate-x-0");
    $chatBtn.addClass("hidden");
  });

  $closeBtn.on("click", function () {
    $chatPanel.addClass("translate-x-full").removeClass("translate-x-0");
    $chatBtn.removeClass("hidden");
  });

  // -------------------------------
  // SEARCH API
  // -------------------------------
  $searchBtn.on("click", async function () {
    const query = $searchInput.val().trim();

    if (!query) {
      alert("Please enter something");
      return;
    }

    try {
      $searchBtn.text("Loading...");
      $searchBtn.prop("disabled", true);

      const response = await fetch("https://shyfit.onrender.com/get-workout", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ query })
      });

      const data = await response.json();

      renderWorkouts(data.workouts);
      renderExercises(data.exercises);
      renderKnowledge(data.knowledge);

      // scroll after results
      $("html, body").animate({
        scrollTop: $workoutContainer.offset().top
      }, 500);

    } catch (err) {
      console.error(err);
      alert("Something went wrong");
    } finally {
      $searchBtn.text("Ask AI");
      $searchBtn.prop("disabled", false);
    }
  });

  // Enter key search
  $searchInput.on("keypress", function (e) {
    if (e.which === 13) {
      $searchBtn.click();
    }
  });

  // -------------------------------
  // CHIP CLICK
  // -------------------------------
  $("section span").on("click", function () {
    $searchInput.val($(this).text());
    $searchBtn.click();
  });

  // -------------------------------
  // RENDER WORKOUTS
  // -------------------------------
  function renderWorkouts(workouts) {
    $workoutContainer.html("");

    workouts.forEach(w => {
      let daysHTML = "";

      for (const day in w.content) {
        const exercises = w.content[day];
        let exerciseList = "";

        if (Array.isArray(exercises)) {
          exercises.forEach(ex => {
            exerciseList += `
              <div class="flex justify-between text-xs py-1 border-b border-gray-100">
                <span class="font-medium text-gray-700">${ex.exercise || ""}</span>
                <span class="text-gray-500">
                  ${ex.sets ? ex.sets + " sets" : ""}
                  ${ex.reps ? " • " + ex.reps + " reps" : ""}
                  ${ex.duration ? " • " + ex.duration : ""}
                </span>
              </div>
            `;
          });
        }

        daysHTML += `
          <div class="bg-gray-50 rounded-lg p-3">
            <p class="text-sm font-semibold text-primary mb-2">${day}</p>
            ${exerciseList}
          </div>
        `;
      }
$workoutContainer.append(`
  <div class="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition-all space-y-4">
    
    <div>
      <h3 class="text-lg font-bold">${w.title}</h3>
      <p class="text-xs text-gray-500 mt-1">
        ${w.goal} • ${w.level}
      </p>

      <button class="ask-coach-btn text-xs text-primary mt-2 underline" data-title="${w.title}">
        Ask Coach about this
      </button>
    </div>

    <div class="grid gap-3">
      ${daysHTML}
    </div>

  </div>
`);
    });
  }

  $(document).on("click", ".ask-coach-btn", function () {
  const title = $(this).data("title");

  $chatInput.val(`Explain this workout: ${title}`);
  sendMessage();

  // open chat
  $chatPanel.removeClass("translate-x-full").addClass("translate-x-0");
  $chatBtn.addClass("hidden");
});

  // -------------------------------
  // RENDER EXERCISES
  // -------------------------------
  function renderExercises(exercises) {
    $exerciseContainer.html("");

    if (!exercises.length) {
      $exerciseContainer.html(`<p class="text-sm text-gray-500">No exercises found.</p>`);
      return;
    }

    exercises.forEach(e => {
      $exerciseContainer.append(`
        <div class="bg-white p-4 rounded-xl shadow">
          <h4 class="font-bold">${e.name}</h4>
          <p class="text-xs text-gray-500">${e.muscles.join(", ")}</p>
        </div>
      `);
    });
  }

  // -------------------------------
  // RENDER KNOWLEDGE
  // -------------------------------
  function renderKnowledge(knowledge) {
    if (!knowledge.length) return;

    const k = knowledge[0];

    $knowledgeContainer.html(`
      <h3 class="text-xl font-bold mb-4">${k.topic}</h3>
      <p class="text-sm">${k.content}</p>
    `);
  }

  // -------------------------------
  // CHAT SYSTEM
  // -------------------------------
  $sendBtn.on("click", sendMessage);

  $chatInput.on("keypress", function (e) {
    if (e.which === 13) {
      sendMessage();
    }
  });

function sendMessage() {
  const message = $chatInput.val().trim();
  if (!message) return;

  // 👤 user message
  addMessage(message, "user");
  $chatInput.val("");

  // 🤖 loading
  const loadingId = addMessage("Typing...", "bot");

  $.ajax({
    url: "https://shyfit.onrender.com/chat",
    method: "POST",
    contentType: "application/json",
    data: JSON.stringify({ query: message }),

    success: function (data) {
      updateMessage(loadingId, data.answer);
    },

    error: function () {
      updateMessage(loadingId, "Something went wrong.");
    }
  });
}

  // -------------------------------
  // CHAT UI HELPERS
  // -------------------------------
  function addMessage(text, sender) {
  const id = Date.now();
  const time = new Date().toLocaleTimeString();

  let html = "";

  if (sender === "user") {
    html = `
      <div class="flex flex-col items-end max-w-[85%] ml-auto">
        <div class="bg-primary text-on-primary p-4 rounded-2xl rounded-tr-none text-sm">
          ${text}
        </div>
        <span class="text-[10px] text-gray-400 mt-1">${time}</span>
      </div>
    `;
  } else {
    html = `
      <div class="flex flex-col items-start max-w-[85%]">
        <div id="msg-${id}" class="bg-surface-container-low text-on-surface p-4 rounded-2xl rounded-tl-none text-sm">
          ${text}
        </div>
        <span class="text-[10px] text-gray-400 mt-1">${time}</span>
      </div>
    `;
  }

  $chatMessages.append(html);

  // 👇 Step 7 integrated here
  $chatMessages.animate({
    scrollTop: $chatMessages[0].scrollHeight
  }, 300);

  return id;
}

  function formatResponse(text) {
  return text
    .replace(/\n/g, "<br>")                // line breaks
    .replace(/\*\*(.*?)\*\*/g, "<b>$1</b>") // bold
    .replace(/- /g, "• ");                 // bullets
}

function typeText(id, text) {
  let i = 0;
  const speed = 15;

  function typing() {
    if (i < text.length) {
      $(`#msg-${id}`).append(text.charAt(i));
      i++;
      setTimeout(typing, speed);
    }
  }

  $(`#msg-${id}`).html("");
  typing();
}

function updateMessage(id, newText) {
  typeText(id, newText);
}

$("#clearChat").on("click", function () {
  $chatMessages.html("");
});
});


