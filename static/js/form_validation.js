odoo.define('custom_module.form_validation', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');

    publicWidget.registry.FormValidation = publicWidget.Widget.extend({
        selector: '.js_job_application_form',

        start: function () {
            console.log("Form validation script started.");  // TODO remove later
            this.$('.s_website_form_send').on('click', this._onFormSubmit.bind(this));
        },

        _onFormSubmit: function (event) {
            console.log("Form submit triggered.");  // TODO remove later

            // Validate each field individually
            var isNameValid = this._validateField('input[name="partner_name"]', '#error_name');
            var isEmailValid = this._validateEmail('input[name="email_from"]', '#error_email');
            var isMobileValid = this._validateField('input[name="partner_mobile"]', '#error_phone');
            var hasCV = this._validateFile('input[name="Resume"]', '#error_resume');

            // Check if all fields are valid
            var allValid = isNameValid && isEmailValid && isMobileValid && hasCV;

            if (hasCV) console.log("CV found!")

            if (!allValid) {
                // event.preventDefault(); // Prevent form submission if any field is invalid
                console.log("Validation failed.");  // TODO remove later
            } else {
                console.log("Validation passed.");  // TODO remove later
                // the actual form submission continues from here
            }
        },

        _validateField: function (fieldSelector, errorSelector) {
            var value = this.$(fieldSelector).val();
            console.log("Validating field:", fieldSelector, "Value:", value);  // TODO remove later
            var isValid = value.trim() !== '';
            this.$(errorSelector).toggle(!isValid);
            return isValid;
        },

        _validateEmail: function (fieldSelector, errorSelector) {
            var email = this.$(fieldSelector).val();
            console.log("Validating email:", email);  // TODO remove later
            var isValid = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/.test(email);
            this.$(errorSelector).toggle(!isValid);
            return isValid;
        },

        _validateFile: function (fieldSelector, errorSelector) {
            var fileInput = this.$(fieldSelector)[0];
            console.log("Validating file input:", fileInput);  // TODO remove later
            var isValid = fileInput && fileInput.files.length > 0;
            this.$(errorSelector).toggle(!isValid);
            return isValid;
        }

    });
});
