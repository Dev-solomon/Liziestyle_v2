document.addEventListener("DOMContentLoaded", function () {
  const orderItems = document.querySelectorAll(".order-item");

  orderItems.forEach((orderItem) => {
    const quantityElement = orderItem.querySelector(".quantity");
    const increaseButton = orderItem.querySelector(".increase-qty");
    const decreaseButton = orderItem.querySelector(".decrease-qty");
    const orderId = orderItem.getAttribute("data-order-id");

    increaseButton.addEventListener("click", function () {
      let quantity = parseInt(quantityElement.textContent);
      quantityElement.textContent = ++quantity;
      sendQuantityToServer(orderId, quantity);
    });

    decreaseButton.addEventListener("click", function () {
      let quantity = parseInt(quantityElement.textContent);
      if (quantity > 1) {
        quantityElement.textContent = --quantity;
        sendQuantityToServer(orderId, quantity);
      }
    });
  });

  function sendQuantityToServer(orderId, quantity) {
    // fetch("/update-quantity", {
    //   method: "POST",
    //   headers: {
    //     "Content-Type": "application/json",
    //   },
    //   body: JSON.stringify({ orderId: orderId, quantity: quantity }),
    // })
    //   .then((response) => response.json())
    //   .then((data) => {
    //     console.log("Success:", data);
    //   })
    //   .catch((error) => {
    //     console.error("Error:", error);
    //   });
  }
});
