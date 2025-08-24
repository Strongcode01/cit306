
(function () {
  // Helpers
  const loader = document.getElementById('global-page-loader');

  function showLoader() {
    if (!loader) return;
    loader.classList.add('show');
    loader.setAttribute('aria-hidden', 'false');
  }

  function hideLoader() {
    if (!loader) return;
    loader.classList.remove('show');
    loader.setAttribute('aria-hidden', 'true');
  }

  // 1) Show loader on normal navigation (clicking internal links)
  function isInternalLink(a) {
    if (!a || !a.getAttribute) return false;
    const href = a.getAttribute('href') || '';
    if (!href || href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('tel:')) return false;
    if (a.target === '_blank' || a.hasAttribute('download') || a.dataset.noSpinner !== undefined) return false;
    // relative links or same-origin absolute links
    try {
      const url = new URL(href, location.href);
      return url.origin === location.origin;
    } catch (e) {
      return true; // treat as internal if URL constructor fails (relative path)
    }
  }

  document.addEventListener('click', function (e) {
    const a = e.target.closest && e.target.closest('a');
    if (!a) return;
    if (!isInternalLink(a)) return;
    // Avoid showing for in-page anchors
    const href = a.getAttribute('href') || '';
    if (href.startsWith('#') && href.length > 1) return;

    // For link clicks that use JS (e.g. single-page nav), letting them behave normally
    // Show spinner briefly for navigation
    showLoader();
    // If navigation is prevented by JS later, pageshow or other logic should hide it.
  }, { capture: true });

  // 2) Show loader on standard form submit
  document.addEventListener('submit', function (e) {
    const form = e.target;
    if (!form || form.dataset.noSpinner !== undefined) return;
    // Let the native submit proceed but show spinner overlay
    showLoader();
    // If the form submission is via AJAX, the JS wrapping fetch/XHR below handles hiding later
  }, { capture: true });

  // 3) Show loader on beforeunload (back/forward/clicking links that cause unload)
  window.addEventListener('beforeunload', function () {
    // browsers may ignore long ops here, but showing overlay gives immediate feedback
    showLoader();
  });

  // 4) Hide loader on page show (including bfcache navigation)
  window.addEventListener('pageshow', function (event) {
    // pageshow runs after navigation back/forward; hide spinner if present
    hideLoader();
  });

  // 5) Intercept fetch and XMLHttpRequest: show loader when active requests >0
  (function wrapNetwork() {
    let activeRequests = 0;
    const originalFetch = window.fetch;
    if (originalFetch) {
      window.fetch = function (...args) {
        activeRequests++;
        showLoader();
        return originalFetch.apply(this, args)
          .then(resp => {
            activeRequests = Math.max(0, activeRequests - 1);
            if (activeRequests === 0) hideLoader();
            return resp;
          })
          .catch(err => {
            activeRequests = Math.max(0, activeRequests - 1);
            if (activeRequests === 0) hideLoader();
            throw err;
          });
      };
    }

    // XHR wrap
    const XHR = window.XMLHttpRequest;
    if (XHR) {
      const origOpen = XHR.prototype.open;
      const origSend = XHR.prototype.send;
      XHR.prototype.open = function () {
        this._shouldTrack = true; // default; you can inspect URL in arguments if you want to skip some requests
        return origOpen.apply(this, arguments);
      };
      XHR.prototype.send = function () {
        if (this._shouldTrack) {
          activeRequests++;
          showLoader();
          this.addEventListener('readystatechange', function () {
            if (this.readyState === 4) {
              activeRequests = Math.max(0, activeRequests - 1);
              if (activeRequests === 0) hideLoader();
            }
          });
        }
        return origSend.apply(this, arguments);
      };
    }
  })();

  // 6) Small safeguard: hide loader after X seconds in case navigation gets stuck
  const SAFETY_TIMEOUT = 15000; // 15s
  let safetyTimer = null;
  function startSafety() {
    clearTimeout(safetyTimer);
    safetyTimer = setTimeout(hideLoader, SAFETY_TIMEOUT);
  }
  function clearSafety() {
    clearTimeout(safetyTimer);
  }

  // wrap show/hide to manage safety
  const _show = showLoader;
  const _hide = hideLoader;
  window.showPageLoader = function () { _show(); startSafety(); };
  window.hidePageLoader = function () { _hide(); clearSafety(); };

  // Make sure loader is hidden on initial load
  document.addEventListener('DOMContentLoaded', hideLoader);
})();

