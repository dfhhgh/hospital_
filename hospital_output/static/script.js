(() => {
  "use strict";

  function qs(selector, root = document) {
    return root.querySelector(selector);
  }

  function createPasswordToggle(input) {
    if (!input || input.dataset.toggleBound === "1") {
      return;
    }

    const wrap = document.createElement("div");
    wrap.style.position = "relative";
    input.parentNode.insertBefore(wrap, input);
    wrap.appendChild(input);

    const btn = document.createElement("button");
    btn.type = "button";
    btn.textContent = "Show";
    btn.setAttribute("aria-label", "Show password");
    btn.style.position = "absolute";
    btn.style.right = "10px";
    btn.style.top = "50%";
    btn.style.transform = "translateY(-50%)";
    btn.style.border = "0";
    btn.style.background = "transparent";
    btn.style.fontSize = "0.82rem";
    btn.style.fontWeight = "700";
    btn.style.cursor = "pointer";
    btn.style.color = "#0f8f84";

    btn.addEventListener("click", () => {
      const isPassword = input.type === "password";
      input.type = isPassword ? "text" : "password";
      btn.textContent = isPassword ? "Hide" : "Show";
      btn.setAttribute(
        "aria-label",
        isPassword ? "Hide password" : "Show password",
      );
    });

    wrap.appendChild(btn);
    input.dataset.toggleBound = "1";
  }

  function bindPreventDoubleSubmit(form, buttonSelector) {
    if (!form) {
      return;
    }

    const submitButton =
      qs(buttonSelector, form) || qs("button[type='submit']", form);
    if (!submitButton) {
      return;
    }

    const defaultText = submitButton.textContent;
    form.addEventListener("submit", () => {
      if (!form.checkValidity()) {
        return;
      }

      submitButton.disabled = true;
      submitButton.textContent = "Processing...";

      window.setTimeout(() => {
        if (!document.hidden) {
          submitButton.disabled = false;
          submitButton.textContent = defaultText;
        }
      }, 7000);
    });
  }

  function initLoginForm() {
    const form = qs("body.login-page form");
    if (!form) {
      return;
    }

    const password = qs("input[name='password']", form);
    createPasswordToggle(password);
    bindPreventDoubleSubmit(form, ".btn-login");
  }

  function initSignupForm() {
    const form = qs("body.signup-page form");
    if (!form) {
      return;
    }

    const password = qs("input[name='password']", form);
    const confirmPassword = qs("input[name='confirm_password']", form);
    const phone = qs("input[name='phone']", form);

    createPasswordToggle(password);
    createPasswordToggle(confirmPassword);

    if (phone) {
      phone.addEventListener("input", () => {
        phone.value = phone.value.replace(/[^0-9+\-\s()]/g, "").slice(0, 20);
      });
    }

    function validatePasswordMatch() {
      if (!password || !confirmPassword) {
        return true;
      }

      if (password.value !== confirmPassword.value) {
        confirmPassword.setCustomValidity("Passwords do not match.");
        return false;
      }

      confirmPassword.setCustomValidity("");
      return true;
    }

    if (password && confirmPassword) {
      password.addEventListener("input", validatePasswordMatch);
      confirmPassword.addEventListener("input", validatePasswordMatch);
    }

    form.addEventListener("submit", (event) => {
      if (!validatePasswordMatch()) {
        event.preventDefault();
        confirmPassword.reportValidity();
      }
    });

    bindPreventDoubleSubmit(form, ".btn-signup");
  }

  document.addEventListener("DOMContentLoaded", () => {
    initLoginForm();
    initSignupForm();
  });
})();
