// this script is to be run in the browser console to check if all
// the img tags are loaded

document.querySelectorAll("img").forEach(img => {
  if (!img.complete || img.naturalWidth === 0) {
    console.log("Unloaded or broken image:", img.src);
  }
});
