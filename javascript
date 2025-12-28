# Scroll when Images ready

function scrollWhenImagesReady(el) {
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
