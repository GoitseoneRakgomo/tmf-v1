/* ============================================
   Insight editor live preview
   ============================================ */

document.addEventListener('DOMContentLoaded', function () {
  var form = document.querySelector('.insight-editor');
  if (!form) return;

  // Elements we watch
  var titleInput = document.getElementById('title');
  var standfirstInput = document.getElementById('standfirst');
  var bodyInput = document.getElementById('body');
  var imageInput = document.getElementById('image_url');
  var typeSelect = document.getElementById('type');
  var colourRadios = document.querySelectorAll('input[name="colour"]');

  // Elements we update
  var previewCard = document.querySelector('.preview-card');
  var previewImageWrap = document.querySelector('.preview-card-image');
  var previewTitle = document.querySelector('.preview-title');
  var authorInput = document.getElementById('author');
  var previewStandfirst = document.querySelector('.preview-standfirst');
  var previewTypeBadge = document.querySelector('.preview-type-badge');
  var previewBody = document.querySelector('.preview-body');
  var previewAuthor = document.querySelector('.preview-meta .author');
  var previewDate = document.querySelector('.preview-meta .date');

  // Set today's date once on load
  if (previewDate) {
    var today = new Date();
    previewDate.textContent = today.toLocaleDateString('en-GB', {
      day: 'numeric', month: 'long', year: 'numeric'
    });
  }

  // --- Live updates ---

  function updateTitle() {
    var val = titleInput.value.trim();
    previewTitle.textContent = val || 'Untitled insight';
  }

  function updateAuthor() {
  if (!authorInput || !previewAuthor) return;
  var val = authorInput.value.trim();
  previewAuthor.textContent = val || 'TMF Staff';
}

  function updateStandfirst() {
    var val = standfirstInput.value.trim();
    previewStandfirst.textContent = val || 'A short standfirst will appear here.';
  }

  function updateBody() {
    var val = bodyInput.value.trim();
    if (!val) {
      previewBody.innerHTML = '<p style="color: var(--muted); font-style: italic;">Body preview will appear here as you type.</p>';
      return;
    }
    // Escape HTML
    var escaped = val
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
    // Split into paragraphs by double newlines
    var paragraphs = escaped.split(/\n\s*\n/).map(function (p) {
      return '<p>' + p.replace(/\n/g, '<br>') + '</p>';
    });
    previewBody.innerHTML = paragraphs.join('');
  }

  function updateType() {
    var val = typeSelect.value;
    previewTypeBadge.textContent = val;
    previewTypeBadge.className = 'preview-type-badge ' + val;
  }

  function updateColour() {
    var checked = document.querySelector('input[name="colour"]:checked');
    if (!checked) return;
    // Remove all colour classes, add the new one
    previewCard.className = 'preview-card colour-' + checked.value;
  }

  function updateImage() {
    var url = imageInput.value.trim();
    if (!url) {
      showPlaceholder('No image yet');
      return;
    }
    // Show loading state
    previewImageWrap.innerHTML = '<div class="preview-image-placeholder">Loading image...</div>';

    var img = new Image();
    img.onload = function () {
      previewImageWrap.innerHTML = '';
      previewImageWrap.appendChild(img);
      img.alt = 'Insight image preview';
    };
    img.onerror = function () {
      showPlaceholder('Image could not be loaded');
    };
    img.src = url;
  }

  function showPlaceholder(message) {
    previewImageWrap.innerHTML =
      '<div class="preview-image-placeholder">' + message + '</div>';
  }

  // --- Bind events ---

  if (titleInput) titleInput.addEventListener('input', updateTitle);
  if (standfirstInput) standfirstInput.addEventListener('input', updateStandfirst);
  if (bodyInput) bodyInput.addEventListener('input', updateBody);
  if (imageInput) imageInput.addEventListener('input', updateImage);
  if (typeSelect) typeSelect.addEventListener('change', updateType);
  if (authorInput) authorInput.addEventListener('input', updateAuthor);
  colourRadios.forEach(function (radio) {
    radio.addEventListener('change', updateColour);
  });

  // --- Initial render ---

  updateTitle();
  updateStandfirst();
  updateBody();
  updateType();
  updateColour();
  updateImage();
  updateAuthor();
});