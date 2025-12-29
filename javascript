# Emoji Picker

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


# Scroll to Bottom when Images ready

function scrollMessagesToBottom() {
    const el = document.getElementById("messages-list");
    if (!el) return;

    const images = el.querySelectorAll("img");
    const scroll = () => el.scrollTo({ top: el.scrollHeight, behavior: "smooth" });

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
