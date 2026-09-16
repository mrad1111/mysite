(function () {
  function normalize(value) {
    if (!value) {
      return '';
    }

    value = String(value).trim().replace(/\s+/g, '');

    var hasComma = value.indexOf(',') !== -1;
    var hasDot = value.indexOf('.') !== -1;

    if (hasComma && hasDot) {
      if (value.lastIndexOf(',') > value.lastIndexOf('.')) {
        value = value.replace(/\./g, '').replace(/,/g, '.');
      } else {
        value = value.replace(/,/g, '');
      }
    } else if (hasComma) {
      var parts = value.split(',');
      if (parts.length > 1 && parts[parts.length - 1].length === 3) {
        value = parts.join('');
      } else {
        value = value.replace(/,/g, '.');
      }
    }

    return value;
  }

  function formatPrice(value) {
    var normalized = normalize(value);
    var num = parseFloat(normalized);

    if (isNaN(num)) {
      return value;
    }

    return num.toLocaleString('en-US', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    });
  }

  function onBlur(event) {
    event.target.value = formatPrice(event.target.value);
  }

  function onFocus(event) {
    event.target.value = normalize(event.target.value);
  }

  document.addEventListener('DOMContentLoaded', function () {
    var input = document.getElementById('id_price');
    if (!input) {
      return;
    }

    input.addEventListener('blur', onBlur);
    input.addEventListener('focus', onFocus);

    if (input.value) {
      input.value = formatPrice(input.value);
    }
  });
})();
