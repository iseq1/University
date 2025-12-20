document.querySelectorAll('.faq details').forEach((item) => {
  item.addEventListener('toggle', (event) => {
    if (event.target.open) {
      document.querySelectorAll('.faq details').forEach((otherItem) => {
        if (otherItem !== event.target) {
          otherItem.removeAttribute('open');
        }
      });
    }
  });
});


const faqs = document.querySelectorAll(".faq-items");

faqs.forEach((faq) => {
  faq.addEventListener("click", () => {
    faqs.forEach((item) => {
      if (item !== faq && item.classList.contains("active")) {
        item.classList.remove("active");
      }
    });

    faq.classList.toggle("active");
  });
});
