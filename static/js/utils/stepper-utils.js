/**
 * Generic 3-step wizard stepper for dashboard Excel/JSON upload modals.
 *
 * Used by: dashboard.html (pages, endpoints, relationships, postman).
 */
(function (global) {
    'use strict';

    /**
     * Create a stepper controller for a 3-step modal wizard.
     *
     * @param {Object} config
     * @param {string[]} config.stepContentIds - IDs for step 1, 2, 3 content divs
     * @param {string[]} [config.stepIndicatorIds] - IDs for step indicator <li> elements (font-medium when active)
     * @param {string[]} [config.stepCircleIds] - IDs for circle <span> elements (active/completed/future styling)
     * @param {Object} config.footerButtonIds - { back, next, sync, close }
     * @param {Object} [config.colors] - { active: 'amber', completed: 'green', future: 'gray' } for circles
     * @returns {{ setStep: function(number), currentStep: function(): number }}
     */
    function createStepper(config) {
        var stepContentIds = config.stepContentIds || [];
        var stepIndicatorIds = config.stepIndicatorIds || [];
        var stepCircleIds = config.stepCircleIds || [];
        var footerButtonIds = config.footerButtonIds || {};
        var colors = config.colors || { active: 'amber', completed: 'green', future: 'gray' };

        var currentStep = 1;

        function setCircle(el, state) {
            if (!el) return;
            el.classList.remove('bg-amber-600', 'bg-green-500', 'bg-gray-300', 'dark:bg-gray-700', 'text-white', 'text-gray-800', 'dark:text-gray-100');
            if (state === 'active') {
                el.classList.add('bg-amber-600', 'text-white');
                el.textContent = el.dataset.num || '';
            } else if (state === 'completed') {
                el.classList.add('bg-green-500', 'text-white');
                el.textContent = '\u2713';
            } else {
                el.classList.add('bg-gray-300', 'dark:bg-gray-700', 'text-gray-800', 'dark:text-gray-100');
                el.textContent = el.dataset.num || '';
            }
        }

        function setStep(step) {
            currentStep = step;

            stepContentIds.forEach(function (id, idx) {
                var el = document.getElementById(id);
                if (el) el.classList.toggle('hidden', step !== idx + 1);
            });

            stepIndicatorIds.forEach(function (id, idx) {
                var el = document.getElementById(id);
                if (el) el.classList.toggle('font-medium', step === idx + 1);
            });

            stepCircleIds.forEach(function (id, idx) {
                var el = document.getElementById(id);
                if (el) {
                    el.dataset.num = String(idx + 1);
                    setCircle(el, step > idx + 1 ? 'completed' : (step === idx + 1 ? 'active' : 'future'));
                }
            });

            var backBtn = document.getElementById(footerButtonIds.back);
            var nextBtn = document.getElementById(footerButtonIds.next);
            var syncBtn = document.getElementById(footerButtonIds.sync);
            var closeBtn = document.getElementById(footerButtonIds.close);

            if (backBtn) backBtn.classList.toggle('hidden', step === 1);
            if (nextBtn) nextBtn.classList.toggle('hidden', step !== 1);
            if (syncBtn) syncBtn.classList.toggle('hidden', step !== 2);
            if (closeBtn) closeBtn.classList.toggle('hidden', step !== 3);
        }

        return {
            setStep: setStep,
            currentStep: function () { return currentStep; }
        };
    }

    global.createStepper = createStepper;
})(typeof window !== 'undefined' ? window : globalThis);
