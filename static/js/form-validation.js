// Lightweight client-side validation helpers — purely for instant visual
// feedback (red border, inline message) before the form is submitted.
// Django's server-side validation remains authoritative; this never
// replaces it, only improves perceived responsiveness.

document.addEventListener("alpine:init", () => {
    Alpine.data("liveValidation", () => ({
        errors: {},

        validateRequired(fieldName, value) {
            if (!value || !value.trim()) {
                this.errors[fieldName] = "This field is required.";
            } else {
                delete this.errors[fieldName];
            }
        },

        validateEmail(fieldName, value) {
            const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (value && !pattern.test(value)) {
                this.errors[fieldName] = "Enter a valid email address.";
            } else {
                delete this.errors[fieldName];
            }
        },

        validatePasswordMatch(password, confirm) {
            if (confirm && password !== confirm) {
                this.errors["password_match"] = "Passwords do not match.";
            } else {
                delete this.errors["password_match"];
            }
        },

        hasError(fieldName) {
            return !!this.errors[fieldName];
        },
    }));
});