document.addEventListener('alpine:init', () => {
    Alpine.data('autocomplete', (category, idField, labelField) => ({
        query: '',
        items: [],
        open: false,
        noMatch: false,
        selectedLabel: '',
        selectedId: '',
        idFieldName: idField || '',
        labelFieldName: labelField || '',

        init() {
            const hidden = this.$el.querySelector('input[type="hidden"]');
            this.selectedId = hidden ? hidden.value : '';
            if (this.labelFieldName) {
                const labelInput = this.$el.querySelector(`input[name="${this.labelFieldName}"]`);
                this.selectedLabel = labelInput ? labelInput.value : '';
            }
        },

        async search() {
            if (this.query.length < 1) {
                this.items = [];
                this.open = false;
                this.noMatch = false;
                return;
            }
            try {
                const resp = await fetch(
                    `/gh-epi-creator/api/lookup/${category}?q=${encodeURIComponent(this.query)}`
                );
                this.items = await resp.json();
                this.open = this.items.length > 0;
                this.noMatch = this.items.length === 0;
            } catch (e) {
                this.items = [];
                this.open = false;
                this.noMatch = false;
            }
        },

        select(item) {
            if (typeof item === 'object') {
                this.selectedLabel = item.label || item.name || item.text || item;
                this.selectedId = item.id || item.code || item.value || '';
            } else {
                this.selectedLabel = item;
                this.selectedId = item;
            }
            this.query = this.selectedLabel;
            this.open = false;
            this.noMatch = false;
            if (this.idFieldName) {
                const hidden = this.$el.querySelector(`input[name="${this.idFieldName}"]`);
                if (hidden) hidden.value = this.selectedId;
            }
            if (this.labelFieldName) {
                const labelInput = this.$el.querySelector(`input[name="${this.labelFieldName}"]`);
                if (labelInput) labelInput.value = this.selectedLabel;
            }
        },

        clear() {
            this.selectedLabel = '';
            this.selectedId = '';
            this.query = '';
            this.noMatch = false;
            if (this.idFieldName) {
                const hidden = this.$el.querySelector(`input[name="${this.idFieldName}"]`);
                if (hidden) hidden.value = '';
            }
            if (this.labelFieldName) {
                const labelInput = this.$el.querySelector(`input[name="${this.labelFieldName}"]`);
                if (labelInput) labelInput.value = '';
            }
        },

        isValid() {
            // A value is valid if the user has selected a known term
            // (selectedId is populated) OR the field is empty.
            return !this.query || !!this.selectedId;
        }
    }));
});

