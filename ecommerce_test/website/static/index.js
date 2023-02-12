function deleteWishlist(wishlistId) {
    fetch("/delete-wishlist", {
      method: "POST",
      body: JSON.stringify({ wishlistId: wishlistId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }