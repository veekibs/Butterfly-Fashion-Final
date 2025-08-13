// This function ensures that the code inside it only runs after the entire HTML document is ready
// This is the jQuery equivalent of 'DOMContentLoaded'
$(document).ready(function(){
  
  // --- Filtering Logic ---
  // Attaches a click event listener to every element with the class 'filter-item'
  $(".filter-item").click(function(){
    // Get the value of the 'data-filter' attribute from the clicked item (e.g., 'all', 'beauty')
    const value = $(this).attr("data-filter");
    
    if (value == "all"){
      // If 'all' is clicked, show all elements with the class 'post-box' with a 1-second animation
      $(".post-box").show("1000");
    }
    else{
      // If a specific category is clicked, first hide all post-boxes that DON'T have that category's class
      $(".post-box").not("." + value).hide("1000");
      // Then, show all post-boxes that DO have that category's class
      $(".post-box." + value).show("1000");
    }
  });
  
  // --- Active Class Logic ---
  // Attaches a click event listener to handle the 'active' visual state
  $(".filter-item").click(function () {
    // Adds the 'active-filter' class to the item that was just clicked
    $(this).addClass("active-filter")
    // Removes the 'active-filter' class from all its sibling elements
    .siblings().removeClass("active-filter");
  });
});