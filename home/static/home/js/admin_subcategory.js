(function () {
  document.addEventListener('DOMContentLoaded', function () {
    var categorySelect = document.getElementById('id_category');
    var subcategorySelect = document.getElementById('id_subcategory');

    if (!categorySelect || !subcategorySelect) {
      return;
    }

    function updateSubcategories(preserveValue) {
      var selectedCategoryId = categorySelect.value;
      var currentVal = subcategorySelect.value;

      if (!selectedCategoryId) {
        subcategorySelect.innerHTML = '<option value="">---------</option>';
        return;
      }

      var url = '/api/subcategories/?category_id=' + encodeURIComponent(selectedCategoryId);

      fetch(url)
        .then(function (res) { return res.json(); })
        .then(function (data) {
          subcategorySelect.innerHTML = '<option value="">---------</option>';
          var foundCurrent = false;

          data.subcategories.forEach(function (sub) {
            var opt = document.createElement('option');
            opt.value = sub.id;
            opt.textContent = sub.name;
            if (preserveValue && String(sub.id) === String(currentVal)) {
              opt.selected = true;
              foundCurrent = true;
            }
            subcategorySelect.appendChild(opt);
          });

          if (preserveValue && !foundCurrent && currentVal) {
            subcategorySelect.value = '';
          }
        })
        .catch(function (err) {
          console.error('Error fetching subcategories:', err);
        });
    }

    // Filter subcategories on page load if category is selected
    if (categorySelect.value) {
      updateSubcategories(true);
    }

    categorySelect.addEventListener('change', function () {
      updateSubcategories(false);
    });
  });
})();
