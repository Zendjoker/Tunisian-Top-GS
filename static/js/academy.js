document.addEventListener("DOMContentLoaded", function () {
    const dropdownToggles = document.querySelectorAll('.dropdownToggle');
    let currentVideo = null;
    let lessonContainers = document.querySelectorAll(".container-lesson");
    const videos = document.querySelectorAll(".videos");
    const modules = document.querySelectorAll(".all-container-steps-modules");
    const videosIDs = [];
    var last_quizz_index = -1;
    var there_is_quizzes = false;
    var quizzes_options_answers = [];
    var right_answers = [];
    const popupMessageCorrect = document.getElementById('popupMessageCorrect');
    const popUpCloseButtonCorrect = document.getElementById('popUpCloseButtonCorrect');
    const popupMessageIncorrect = document.getElementById('popupMessageIncorrect');
    const popUpCloseButtonIncorrect = document.getElementById('popUpCloseButtonIncorrect');

    const lockedCourseMessage = document.getElementById('lockedCourseMessage');
    const returnToPreviousStep = document.getElementById('returnToPreviousStep');

    popUpCloseButtonCorrect.addEventListener('click', function () {
        popupMessageCorrect.style.display = 'none';
    });

    popUpCloseButtonIncorrect.addEventListener('click', function () {
        popupMessageIncorrect.style.display = 'none';
    });

    returnToPreviousStep.addEventListener('click', function () {
        lockedCourseMessage.style.display = 'none';
        showLesson(lessonContainers, 0, "PreviousStep");
    });

    // Fetching level progression
    ajaxRequest("POST", "/level_progress/", { level_id: level_id }, function (response) {
        updateProgress(response.level_progression);
    }, null, false, "level progression", null);

    // Adding click event listeners to videos
    videos.forEach(function (video) {
        const videoID = video.dataset.id;
        videosIDs.push(videoID);

        video.addEventListener("click", function (e) {
            e.preventDefault();
            if (video.classList.contains('locked')) {
                lockedCourseMessage.style.display = 'block';
                lessonContainers.forEach(container => container.style.display = 'none');
            } else {
                changeVideo(videoID);
                showLesson(lessonContainers, 0, "24");
                lockedCourseMessage.style.display = 'none';
            }
        });
    });

    // Setting the current video to the first video
    currentVideo = videosIDs[0];
    changeVideo(currentVideo);

    // Handling URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const videoIdParam = urlParams.get("id");
    let videoId = videosIDs.length > 0 ? videosIDs[0] : null;
    if (videoIdParam && videosIDs.includes(videoIdParam)) {
        videoId = videoIdParam;
        changeVideo(videoId);
    }

    const finishStepBttn = document.querySelector("#finishStep");
    if (finishStepBttn) {
        finishStepBttn.addEventListener("click", function (e) {
            e.preventDefault();
            finishVideo(currentVideo, lessonContainers);
        });
    } else {
        console.error("#finishStep button not found");
    }

    document.querySelectorAll(".iconlike").forEach(function (element) {
        toggleLikeCss(element);
        element.addEventListener("click", function (event) {
            toggleLike(event.currentTarget);
        });
    });

    function toggleLike(element) {
        ajaxRequest("post", "/is_video_liked/", { video_id: currentVideo }, function (response) {
            if (response.is_liked) {
                ajaxRequest("post", "/remove_liked_video/", { video_id: currentVideo }, function () {
                    toggleLikeCss(element);
                }, null, false, "Like video", null);
            } else {
                ajaxRequest("post", "/add_liked_video/", { video_id: currentVideo }, function () {
                    toggleLikeCss(element);
                }, null, false, "Dislike video", null);
            }
        }, null, false, "Toggle like video", null);
    }

    function toggleLikeCss(element) {
        ajaxRequest("post", "/is_video_liked/", { video_id: currentVideo }, function (response) {
            if (response.is_liked) {
                element.classList.add("liked");
            } else {
                element.classList.remove("liked");
            }
        }, null, false, "Toggle like video", null);
    }

    function updateProgress(percentage) {
        const levelProgressText = document.querySelector(".percentage-progess");
        const progressBar = document.getElementById("progressBar");
        if (levelProgressText) {
            levelProgressText.innerText = `${percentage}% complete`;
        }
        if (progressBar) {
            progressBar.style.width = percentage + "%";
        }
    }

    function showLesson(lessonContainers, index, whereitscalled) {
        console.log("showLesson, index: " + index + " " + whereitscalled);
        lessonContainers.forEach((container, i) => {
            container.style.display = i === index ? "flex" : "none";
        });
    }

    function changeVideo(videoId) {
        if (!videoId) {
            console.error("changeVideo: videoId is undefined");
            return;
        }

        currentVideo = videoId;

        ajaxRequest("POST", "/get-video/", { videoId: videoId }, function (response) {
            if (response.success && response.video) {
                const videoSRC = document.querySelector(".videoSRC");
                var lesson_video_conttainer = document.querySelector(".lesson-video")
                if (response.video.vimeo_url) {
                    lesson_video_conttainer.innerHTML = `
                        <div><iframe src="${response.video.vimeo_url}?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479" frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write" title="${response.video.title}"></iframe></div>`;
                    
                } 
                else if (response.video.video_file) {
                    lesson_video_conttainer.innerHTML = `
                        <video controls>
                            <source class="videoSRC" src="${response.video.video_file}" type="video/mp4">
                        </video>`;
                    
                } 
                else if (response.video.video_image) {
                    lesson_video_conttainer.innerHTML = `<img src="${response.video.video_image}" alt="">`;
                }
                else {
                    lesson_video_conttainer.innerHTML = ""
                }
                /* if (videoSRC) {
                    videoSRC.src = response.video.video_file;
                    document.querySelector("video").load();
                } */

                document.querySelectorAll(".video-title").forEach((el) => {
                    if (el) el.innerText = response.video.title;
                });
                document.querySelectorAll(".description-step-video").forEach((el) => {
                    if (el) el.innerHTML = response.video.notes;
                });
                document.querySelectorAll(".content-text-inside").forEach((el) => {
                    if (el) el.innerHTML = response.video.summary;
                });
                Prism.highlightAll();
                loadQuiz(videoId);

                document.querySelectorAll('.step').forEach(step => {
                    step.classList.remove('active-step');
                });
                const currentStepElement = document.querySelector(`.videos[data-id='${videoId}'] .step`);
                if (currentStepElement) {
                    currentStepElement.classList.add('active-step');
                }
                lessonContainers = document.querySelectorAll(".container-lesson"); // Update lessonContainers NodeList
            } else {
                displayFeedbackMessage("Error loading video data. Please try again.", false);
            }
        }, null, false, "get video details", null);
    }

    function loadQuiz(videoId) {
        ajaxRequest("POST", "/get-video/", { videoId: videoId }, function (response) {
            if (response.success && response.video && response.video.quizes) {
                generateAnswers(response.video.quizes);
            } else {
                displayFeedbackMessage("Error loading quiz data. Please try again.", false);
            }
        }, function () {
            displayFeedbackMessage("Error loading quiz data. Please try again.", false);
        }, false, "Load quiz", null);
    }

    function generateAnswers(quizzes) {
        console.log("Generating", quizzes)
        const quizzesNextDiv = document.querySelector('.quizzes_next');
        quizzes_options_answers = [];
        right_answers = [];
        // Remove existing quiz containers
        const quizzes_containers = document.querySelectorAll(".container-quiz");
        quizzes_containers.forEach((quiz_container) => {
            quiz_container.remove();
        });

        if (quizzes.length > 0) {
            there_is_quizzes = true;
            // Step 1: Create an array to hold the quiz containers
            const quizContainers = [];
            // Create the quiz containers and store them in the array
            quizzes.forEach((quizz, index) => {
                last_quizz_index = index + 2;
                right_answers.push(quizz.correct_option_id);
                const prev_index = index + 1;
                const next_index = index + 3;

                const quiz_container = document.createElement("div");
                quiz_container.classList.add("container-quiz", "container-lesson");

                const lessons_containers = document.createElement("div");
                lessons_containers.classList.add("content-video-lesson");

                const title_default_quiz = document.createElement("div");
                title_default_quiz.classList.add("title-default-quiz");
                title_default_quiz.innerHTML = `<span class="text-default-quiz">QUIZZES</span>`;

                lessons_containers.appendChild(title_default_quiz);

                const fill_question = document.createElement("div");
                fill_question.classList.add("fill-question");

                const quiz_question = document.createElement("div");
                quiz_question.classList.add("quiz-question");
                quiz_question.innerText = quizz.question;
                fill_question.appendChild(quiz_question);

                const container_answers = document.createElement("ul");
                container_answers.classList.add("container-answers");

                // Collect options
                const options_containers = [];

                quizz.options.forEach((option) => {
                    const answer_option = document.createElement("li");
                    answer_option.classList.add("option-container", "answer-option");
                    answer_option.setAttribute('data-option-id', option.id);

                    if (option.text) {
                        const spanElement = document.createElement('span');
                        spanElement.className = 'span-answers-quiz';
                        spanElement.innerText = option.text;
                        answer_option.appendChild(spanElement);
                    }

                    if (option.img) {
                        const imgElement = document.createElement('img');
                        imgElement.className = 'img-answers-quiz';
                        imgElement.src = option.img;
                        answer_option.appendChild(imgElement);
                    }
                    options_containers.push(answer_option);
                });

                // Append options and add event listeners
                options_containers.forEach((answer_option) => {
                    quizzes_options_answers[index] = null;
                    answer_option.addEventListener("click", (e) => {
                        const is_selected = answer_option.classList.contains("selected");
                        options_containers.forEach((answer_optionv2) => {
                            answer_optionv2.classList.remove("selected");
                        });
                        if (!is_selected) {
                            answer_option.classList.add("selected");
                            quizzes_options_answers[index] = answer_option.getAttribute('data-option-id');
                        } else {
                            quizzes_options_answers[index] = null;
                        }
                        console.log(quizzes_options_answers);
                    });
                    container_answers.appendChild(answer_option);
                });

                fill_question.appendChild(container_answers);
                lessons_containers.appendChild(fill_question);

                const next_lesson = document.createElement('div');
                next_lesson.classList.add('next-lesson');

                const prev_container = document.createElement('div');
                const prev_button = document.createElement('a');
                prev_button.classList.add("prev-btn", "prev-next-bttn");
                prev_button.setAttribute('data-index', prev_index);
                prev_button.innerHTML = `<img src="/static/assets/back.svg" alt="arrow-left" />BACK`;
                prev_container.appendChild(prev_button);
                next_lesson.appendChild(prev_container);

                const next_container = document.createElement('div');
                const next_button = document.createElement('a');
                next_button.classList.add("keep-next", "prev-next-bttn", "quizz-next-page-btn");
                next_button.setAttribute('data-index', next_index);
                next_button.innerHTML = `NEXT <img src="/static/assets/next.svg" alt="arrow-right" />`;
                next_container.appendChild(next_button);
                next_lesson.appendChild(next_container);

                quiz_container.appendChild(lessons_containers);
                quiz_container.appendChild(next_lesson);

                // Store the created quiz container in the array
                quizContainers.push(quiz_container);
            });

            // Step 2: Append the quiz containers in reverse order
            quizContainers.reverse().forEach((quiz_container) => {
                quizzesNextDiv.parentNode.insertBefore(quiz_container, quizzesNextDiv.nextSibling);
            });

            document.querySelector(".last-back").setAttribute("data-index", last_quizz_index)
        }
        else {
            there_is_quizzes = false;
            document.querySelector(".last-back").setAttribute("data-index", 1)
        }

        // Update lessonContainers NodeList
        lessonContainers = document.querySelectorAll(".container-lesson");

        document.querySelectorAll(".prev-next-bttn").forEach(function (btn) {
            btn.addEventListener("click", function (e) {
                e.preventDefault();
                const index = parseInt(btn.getAttribute("data-index"));
                showLesson(lessonContainers, index, "327");
            });
        });

        document.querySelectorAll(".prev-next-bttn").forEach(function (btn) {
            btn.addEventListener("click", function (e) {
                e.preventDefault();
                const index = parseInt(btn.getAttribute("data-index"));
                console.log(quizzes_options_answers);
                if (index == last_quizz_index + 1 && there_is_quizzes) {
                    if (quizzes_options_answers.includes(null)) {
                        loadQuiz(currentVideo);
                        showLesson(lessonContainers, 0, "339");
                        displayPopupMessageIncorrect("You have to answer all quizzes");
                    } else {
                        var quizz_passed = true;

                        quizzes_options_answers.forEach((answer, index) => {
                            if (answer != parseInt(right_answers[index])) {
                                quizz_passed = false;
                            }
                        });
                        console.log("is quizz passed?: ", quizz_passed);
                        if (quizz_passed) {
                            showLesson(lessonContainers, index, "359");
                            displayPopupMessageCorrect("You have answered all quizzes correctly. Well done!");
                        } else {
                            loadQuiz(currentVideo);
                            showLesson(lessonContainers, 0, "364");
                            displayPopupMessageIncorrect("You need to pass all quizzes correctly to proceed to the next step.");
                        }
                    }
                } else {
                    showLesson(lessonContainers, index, "369");
                }
            });
        });
        showLesson(lessonContainers, 0, "372");
    }

    function displayPopupMessageCorrect(message) {
        const popupSpanCorrect = document.getElementById('popupSpanCorrect');
        popupSpanCorrect.innerText = message;
        popupMessageCorrect.style.display = 'flex';
        setTimeout(() => {
            popupMessageCorrect.style.display = 'none';
        }, 2000);
    }

    function displayPopupMessageIncorrect(message) {
        const popupSpanIncorrect = document.getElementById('popupSpanIncorrect');
        popupSpanIncorrect.innerText = message;
        popupMessageIncorrect.style.display = 'flex';
        setTimeout(() => {
            popupMessageIncorrect.style.display = 'none';
        }, 2000);
    }

    function finishVideo(video_id, lessonContainers) {
        ajaxRequest("POST", "/videoFinished/", { videoId: video_id }, function (response) {
            if (response.success) {
                ajaxRequest("POST", "/level_progress/", { level_id: level_id }, function (response) {
                    updateProgress(response.level_progression);
                }, null, true, "level progression", null);

                videos.forEach(function (video) {
                    const videoID = video.dataset.id;
                    ajaxRequest("POST", "/get_video_icon/", { video_id: videoID }, function (response) {
                        video.classList.remove("completed");
                        video.classList.remove("open");
                        video.classList.remove("locked");
                        video.classList.add(response.icon);
                        const videoIcon = video.querySelector(".video_icon");
                        if (videoIcon) {
                            videoIcon.src = static_url + "assets/" + response.icon + ".png";
                        }
                    }, null, true, "change video icons", null);
                });

                modules.forEach(function (module) {
                    let dropdown = module.querySelector(".dropdown-modules");
                    const moduleID = dropdown.getAttribute("data-id");

                    if (moduleID) {
                        ajaxRequest("POST", "/get_module_icon/", { module_id: moduleID }, function (response) {
                            dropdown.classList.remove("completed");
                            dropdown.classList.remove("open");
                            dropdown.classList.remove("locked");
                            dropdown.classList.add(response.icon);
                            const moduleIcon = module.querySelector(".module_icon");
                            if (moduleIcon) {
                                moduleIcon.src = static_url + "assets/" + response.icon + ".png";
                            }
                        }, null, true, "change video icons", null);
                    } else {
                        console.error('Module ID is null or undefined for module:', module);
                    }
                });

                if (response.success) {
                    if (response.next_step) {
                        changeVideo(response.next_step.video_id);
                        showLesson(lessonContainers, 0, "423");
                    } else {
                        if (response.video_in_next_module === false) {
                            window.location.href = `/courses/${response.url_title}/levels?fid=2`;
                        } else if (response.level_finished === true) {
                            window.location.href = `/courses/${response.url_title}/levels?fid=0`;
                        } else if (response.finished_open_modules === true) {
                            window.location.href = `/courses/${response.url_title}/levels?fid=1`;
                        } else {
                            window.location.href = `/courses/${response.url_title}/levels?fid=3`;
                        }
                    }
                } else {
                    window.location.href = `/courses/${response.url_title}/levels?fid=4`;
                }
            } else {
                window.location.href = `/courses/${response.url_title}/levels?fid=5`;
            }
        }, null, true, "video finished", null);
    }

    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function (event) {
            event.preventDefault();
            const arrowIcon = toggle.querySelector('.arrow-icon');
            const modulesDropdowns = toggle.parentElement.nextElementSibling;

            arrowIcon.classList.toggle('rotate');
            modulesDropdowns.classList.toggle('opened');
        });
    });

    lessonContainers = document.querySelectorAll(".container-lesson"); // Update lessonContainers NodeList

    document.querySelectorAll(".prev-next-bttn").forEach(function (btn) {
        btn.addEventListener("click", function (e) {
            e.preventDefault();
            const index = parseInt(btn.getAttribute("data-index"));
            showLesson(lessonContainers, index, "451");
        });
    });

    videos.forEach(function (video) {
        const videoID = video.dataset.id;
        ajaxRequest("POST", "/get_video_icon/", { video_id: videoID }, function (response) {
            video.classList.remove("completed");
            video.classList.remove("open");
            video.classList.remove("locked");
            video.classList.add(response.icon);
            const videoIcon = video.querySelector(".video_icon");
            if (videoIcon) {
                videoIcon.src = static_url + "assets/" + response.icon + ".png";
            }
        }, null, true, "change video icons", null);
    });

    modules.forEach(function (module) {
        let dropdown = module.querySelector(".dropdown-modules");
        const moduleID = dropdown.getAttribute("data-id");

        if (moduleID) {
            ajaxRequest("POST", "/get_module_icon/", { module_id: moduleID }, function (response) {
                dropdown.classList.remove("completed");
                dropdown.classList.remove("open");
                dropdown.classList.remove("locked");
                dropdown.classList.add(response.icon);
                const moduleIcon = module.querySelector(".module_icon");
                if (moduleIcon) {
                    moduleIcon.src = static_url + "assets/" + response.icon + ".png";
                }
            }, null, true, "change video icons", null);
        } else {
            console.error('Module ID is null or undefined for module:', module);
        }
    });
});
