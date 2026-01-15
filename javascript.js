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




