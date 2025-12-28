# Emoji Picker

<script src="https://cdn.jsdelivr.net/npm/emoji-mart@latest/dist/browser.js"></script>

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


# Scroll when Images ready

function scrollToBottom(el) {
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
