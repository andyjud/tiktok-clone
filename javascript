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


# Reset is_live to False

// Reset the user's is_live status after page refresh
window.addEventListener("beforeunload", () => {
    fetch("{% url 'reset_live' %}", {
        method: "POST",
        headers: {"X-CSRFToken": "{{ csrf_token }}"}
    });
});
