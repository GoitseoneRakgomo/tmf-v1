/* ============================================
   Programme editor live preview
   ============================================ */

document.addEventListener('DOMContentLoaded', function () {
  var form = document.querySelector('.programme-editor');
  if (!form) return;

  // ---------- Inputs ----------
  var kindSelect = document.getElementById('kind');
  var categorySelect = document.getElementById('category');
  var titleInput = document.getElementById('title');
  var standfirstInput = document.getElementById('standfirst');
  var bodyInput = document.getElementById('body');
  var dateInput = document.getElementById('date');
  var endDateInput = document.getElementById('end_date');
  var timeInput = document.getElementById('time');
  var placeInput = document.getElementById('place');
  var venueInput = document.getElementById('venue');
  var priceInput = document.getElementById('price');
  var priceLabelInput = document.getElementById('price_label');
  var capacityInput = document.getElementById('capacity');
  var registerInput = document.getElementById('register_url');
  var imageInput = document.getElementById('image_url');
  var facilitatorInput = document.getElementById('facilitator');
  var formatSelect = document.getElementById('format');
  var durationInput = document.getElementById('duration');
  var outlineInput = document.getElementById('outline');
  var outcomesInput = document.getElementById('outcomes');
  var colourRadios = document.querySelectorAll('input[name="colour"]');

  // ---------- Preview elements ----------
  var preview = document.querySelector('.programme-preview');
  var previewHero = document.querySelector('.programme-preview-hero');
  var previewTitle = document.querySelector('.programme-preview-title');
  var previewStandfirst = document.querySelector('.programme-preview-standfirst');

  var metaDate = document.querySelector('.meta-date');
  var metaTime = document.querySelector('.meta-time');
  var metaPlace = document.querySelector('.meta-place');
  var metaVenue = document.querySelector('.meta-venue');

  var previewPriceValue = document.querySelector('.price-value');
  var previewCta = document.querySelector('.programme-preview-cta');

  var previewCapacity = document.querySelector('.programme-preview-capacity');
  var previewCapacityText = document.querySelector('.programme-preview-capacity .cap-text strong');
  var previewCapacityBar = document.querySelector('.programme-preview-capacity .bar span');

  var previewDescription = document.querySelector('.programme-preview-section.description');

  var previewCourseExtras = document.querySelector('.programme-preview-section.course-extras');
  var previewFacilitator = document.querySelector('.course-facilitator');
  var previewFormat = document.querySelector('.course-format');
  var previewDuration = document.querySelector('.course-duration');
  var previewOutline = document.querySelector('.course-outline');
  var previewOutcomes = document.querySelector('.course-outcomes');

  // ---------- Helpers ----------

  function formatDate(iso) {
    if (!iso) return '—';
    var d = new Date(iso);
    if (isNaN(d.getTime())) return iso;
    return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function renderRibbon() {
    var kind = kindSelect ? kindSelect.value : 'event';
    var cat = categorySelect ? categorySelect.value : 'talk';
    return (
      '<div class="hero-ribbon">' +
        '<span class="preview-badge ' + escapeHtml(kind) + '">' + escapeHtml(kind) + '</span>' +
        '<span class="preview-badge category">' + escapeHtml(cat) + '</span>' +
      '</div>'
    );
  }

  // ---------- Updates ----------

  function updateKind() {
    if (!kindSelect) return;
    var kind = kindSelect.value;
    if (previewCta) previewCta.textContent = kind === 'course' ? 'Book now' : 'Register';
    if (previewCourseExtras) {
      if (kind === 'course') previewCourseExtras.classList.remove('is-hidden');
      else previewCourseExtras.classList.add('is-hidden');
    }
    updateImage(); // re-render ribbon with new kind
    updateCategory();
  }

  function updateCategory() {
    if (!categorySelect) return;
    // Category badge lives inside the hero, so re-render the hero
    // Only update the badge in place if it exists
    var badge = previewHero && previewHero.querySelector('.preview-badge.category');
    if (badge) badge.textContent = categorySelect.value;
    updateImage();
  }

  function updateTitle() {
    var val = titleInput ? titleInput.value.trim() : '';
    if (previewTitle) previewTitle.textContent = val || 'Untitled programme';
  }

  function updateStandfirst() {
    var val = standfirstInput ? standfirstInput.value.trim() : '';
    if (previewStandfirst) previewStandfirst.textContent = val || 'A short summary will appear here.';
  }

  function updateDate() {
    if (!metaDate) return;
    var start = dateInput ? dateInput.value : '';
    var end = endDateInput ? endDateInput.value : '';
    if (!start) {
      metaDate.textContent = '—';
    } else if (end && end !== start) {
      metaDate.textContent = formatDate(start) + ' – ' + formatDate(end);
    } else {
      metaDate.textContent = formatDate(start);
    }
  }

  function updateTime() {
    if (!metaTime) return;
    var val = timeInput ? timeInput.value.trim() : '';
    metaTime.textContent = val || '—';
  }

  function updatePlace() {
    if (!metaPlace) return;
    var val = placeInput ? placeInput.value.trim() : '';
    metaPlace.textContent = val || '—';
  }

  function updateVenue() {
    if (!metaVenue) return;
    var val = venueInput ? venueInput.value.trim() : '';
    metaVenue.textContent = val || '—';
  }

  function updatePrice() {
    if (!previewPriceValue) return;
    var label = priceLabelInput ? priceLabelInput.value.trim() : '';
    if (!label) {
      var num = parseInt(priceInput ? priceInput.value : '0', 10) || 0;
      label = num === 0 ? 'Free' : 'R' + num.toLocaleString();
    }
    previewPriceValue.textContent = label;
  }

  function updateCapacity() {
    if (!previewCapacity) return;
    var cap = parseInt(capacityInput ? capacityInput.value : '0', 10) || 0;
    if (cap === 0) {
      previewCapacity.classList.add('is-hidden');
      return;
    }
    previewCapacity.classList.remove('is-hidden');
    if (previewCapacityText) previewCapacityText.textContent = cap;
    if (previewCapacityBar) previewCapacityBar.style.width = '0%';
  }

  function updateDescription() {
    if (!previewDescription) return;
    var val = bodyInput ? bodyInput.value.trim() : '';
    if (!val) {
      previewDescription.classList.add('is-hidden');
      return;
    }
    previewDescription.classList.remove('is-hidden');

    // Escape HTML, then split into paragraphs on blank lines
    var escaped = escapeHtml(val);
    var paragraphs = escaped.split(/\n\s*\n/).map(function (p) {
      return '<p>' + p.replace(/\n/g, '<br>') + '</p>';
    });

    // Rebuild section (keep the <h4>)
    previewDescription.innerHTML = '<h4>Description</h4>' + paragraphs.join('');
  }

  function updateCourseExtras() {
    if (!previewCourseExtras) return;
    var kind = kindSelect ? kindSelect.value : 'event';
    if (kind !== 'course') return;

    if (previewFacilitator) previewFacilitator.textContent = (facilitatorInput && facilitatorInput.value.trim()) || '—';
    if (previewFormat) previewFormat.textContent = (formatSelect && formatSelect.value) || '—';
    if (previewDuration) previewDuration.textContent = (durationInput && durationInput.value.trim()) || '—';
    if (previewOutline) previewOutline.textContent = (outlineInput && outlineInput.value.trim()) || '—';
    if (previewOutcomes) previewOutcomes.textContent = (outcomesInput && outcomesInput.value.trim()) || '—';
  }

  function updateColour() {
    if (!preview) return;
    var checked = document.querySelector('input[name="colour"]:checked');
    if (!checked) return;
    preview.className = 'programme-preview colour-' + checked.value;
  }

  function updateImage() {
    if (!previewHero) return;
    var url = imageInput ? imageInput.value.trim() : '';

    if (!url) {
      previewHero.innerHTML = renderRibbon() + '<div class="preview-image-placeholder">No image yet</div>';
      return;
    }

    previewHero.innerHTML = renderRibbon() + '<div class="preview-image-placeholder">Loading image...</div>';

    var img = new Image();
    img.onload = function () {
      previewHero.innerHTML = renderRibbon();
      previewHero.appendChild(img);
      img.alt = 'Programme image preview';
    };
    img.onerror = function () {
      previewHero.innerHTML = renderRibbon() + '<div class="preview-image-placeholder">Image could not be loaded</div>';
    };
    img.src = url;
  }

  // ---------- Bind events ----------

  if (kindSelect) {
    kindSelect.addEventListener('change', updateKind);
  }
  if (categorySelect) {
    categorySelect.addEventListener('change', updateCategory);
  }
  if (titleInput) titleInput.addEventListener('input', updateTitle);
  if (standfirstInput) standfirstInput.addEventListener('input', updateStandfirst);
  if (bodyInput) bodyInput.addEventListener('input', updateDescription);
  if (dateInput) dateInput.addEventListener('change', updateDate);
  if (endDateInput) endDateInput.addEventListener('change', updateDate);
  if (timeInput) timeInput.addEventListener('input', updateTime);
  if (placeInput) placeInput.addEventListener('input', updatePlace);
  if (venueInput) venueInput.addEventListener('input', updateVenue);
  if (priceInput) priceInput.addEventListener('input', updatePrice);
  if (priceLabelInput) priceLabelInput.addEventListener('input', updatePrice);
  if (capacityInput) capacityInput.addEventListener('input', updateCapacity);
  if (imageInput) imageInput.addEventListener('input', updateImage);

  if (facilitatorInput) facilitatorInput.addEventListener('input', updateCourseExtras);
  if (formatSelect) formatSelect.addEventListener('change', updateCourseExtras);
  if (durationInput) durationInput.addEventListener('input', updateCourseExtras);
  if (outlineInput) outlineInput.addEventListener('input', updateCourseExtras);
  if (outcomesInput) outcomesInput.addEventListener('input', updateCourseExtras);

  colourRadios.forEach(function (radio) {
    radio.addEventListener('change', updateColour);
  });

  // ---------- Initial render ----------

  updateKind();
  updateTitle();
  updateStandfirst();
  updateDate();
  updateTime();
  updatePlace();
  updateVenue();
  updatePrice();
  updateCapacity();
  updateDescription();
  updateCourseExtras();
  updateColour();
  updateImage();
});