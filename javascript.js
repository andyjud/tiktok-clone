// Emoji Picker

<script defer src="https://cdn.jsdelivr.net/npm/emoji-mart@latest/dist/browser.js"></script>

function emojiPicker() {
  return {
    emojiOpen: false,
    picker: null,
    emojiToggle() {
      this.emojiOpen = !this.emojiOpen
      if (this.emojiOpen && !this.picker) {
        this.picker = new EmojiMart.Picker({
          onEmojiSelect: emoji => {
            this.$refs.messageInput.value += emoji.native;
          }
        })
        this.$refs.pickerContainer.appendChild(this.picker)
      }
    }
  }
}


// Scroll to Bottom when Images ready

function scrollMessagesToBottom() {
  const el = document.getElementById("messages-list");
    if (!el) return;

  const images = el.querySelectorAll("img");
  const scroll = () => el.scrollTop = el.scrollHeight;

  if (!images.length) return scroll();

  let loaded = 0;
  images.forEach(img => {
    if (img.complete) {
      loaded++;
    } else {
      img.addEventListener("load", () => {
        loaded++;
        if (loaded === images.length) scroll();
      }, { once: true });
    }
  });

  if (loaded === images.length) scroll();
}


---------------------
VIDEO
---------------------

// Upload component for videos and images

<script>
    function uploadComponent() {
        return {
            isDragging: false,
            fileUrl: null,
            fileType: null,
            caption: '',
            hashtag: '',

            fileDropped(event) {
                event.preventDefault();
                this.isDragging = false;
                const file = event.dataTransfer.files[0];
                if (file && (file.type.startsWith('image/') || file.type.startsWith('video/'))) {
                    this.previewFile(file);
                }
            },

            fileSelected(event) {
                const file = event.target.files[0];
                if (file && (file.type.startsWith('image/') || file.type.startsWith('video/'))) {
                    this.previewFile(file);
                }
            },

            previewFile(file) {
                this.fileUrl = URL.createObjectURL(file);
                this.fileType = file.type.startsWith('image/') ? 'image' : 'video';
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(file);
                this.$refs.inputFileSelected.files = dataTransfer.files;
            },

            discardUpload() {
                this.fileUrl = null;
                this.fileType = null;
                this.caption = '';
                this.hashtag = '';
                this.$refs.inputFileSelected.value = '';
            }
        }
    }
</script>



// VIDEO PLAYER COMPONENT

<script>

window.userWantsSound = false;
window.currentlyPlayingVideo = null;

function videoPlayer(src) {
    return {
        src,
        playing: false,
        muted: true,
        userPaused: false,
        ready: false,

        init() {
            const video = this.$refs.videoPlayer;

            this.muted = !window.userWantsSound;
            video.muted = this.muted;

            this.observeVideo(video);
            this.ready = true;
        },

        observeVideo(video) {
            const observer = new IntersectionObserver(([entry]) => {
                if (window.pauseAllVideosFlag) {
                    // If modal is open, force pause and mute
                    video.pause();
                    video.muted = true;
                    return;
                }

                if (entry.isIntersecting && !this.userPaused) {
                    this.muted = !window.userWantsSound;
                    video.muted = this.muted;

                    if (window.currentlyPlayingVideo && window.currentlyPlayingVideo !== video) {
                        window.currentlyPlayingVideo.pause();
                    }

                    window.currentlyPlayingVideo = video;
                    video.play().catch(() => {});
                } else if (!entry.isIntersecting) {
                    if (window.currentlyPlayingVideo === video) {
                        window.currentlyPlayingVideo = null;
                    }
                    video.pause();
                }
            }, { threshold: 0.6 });
            observer.observe(video);
        },

        togglePlay() {
            const video = this.$refs.videoPlayer;
            if (video.paused) {
                this.userPaused = false;
                if (window.currentlyPlayingVideo && window.currentlyPlayingVideo !== video) {
                    window.currentlyPlayingVideo.pause();
                }
                window.currentlyPlayingVideo = video;
                video.play();
            } else {
                this.userPaused = true;
                video.pause();
                if (window.currentlyPlayingVideo === video) window.currentlyPlayingVideo = null;
            }
        },

        toggleMute() {
            const video = this.$refs.videoPlayer;
            this.muted = !this.muted;
            video.muted = this.muted;
            window.userWantsSound = !this.muted;
        }
    }
}

function modalVideoController() {
    return {
        init() {
            this.$watch('modalPage', value => {
                if (value) {
                    this.stopVideos(); // pause & mute all videos when modal opens
                }
            });
        },

        stopVideos() {
            document.querySelectorAll('video[x-ref="videoPlayer"]').forEach(video => {
                video.pause();
                video.muted = true;
            });
        },
    }
}

document.body.addEventListener('htmx:afterSwap', (e) => {
    if (e.target.id !== 'modalpage-content') return;
    document.querySelectorAll('video[x-ref="videoPlayer"]').forEach(video => {
        video.pause();
        video.muted = true;
        video.load();
    });
});

</script>





