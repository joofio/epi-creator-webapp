document.addEventListener('alpine:init', () => {
    Alpine.data('autocomplete', (category, idField) => ({
        query: '',
        items: [],
        open: false,
        selectedLabel: '',
        selectedId: '',
        idFieldName: idField || '',

        init() {
            const hidden = this.$el.querySelector('input[type="hidden"]');
            this.selectedId = hidden ? hidden.value : '';
        },

        async search() {
            if (this.query.length < 1) {
                this.items = [];
                this.open = false;
                return;
            }
            try {
                const resp = await fetch(
                    `/gh-epi-creator/api/lookup/${category}?q=${encodeURIComponent(this.query)}`
                );
                this.items = await resp.json();
                this.open = this.items.length > 0;
            } catch (e) {
                this.items = [];
                this.open = false;
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
            this.query = '';
            this.open = false;
            if (this.idFieldName) {
                const hidden = this.$el.querySelector(`input[name="${this.idFieldName}"]`);
                if (hidden) hidden.value = this.selectedId;
            }
        },

        clear() {
            this.selectedLabel = '';
            this.selectedId = '';
            this.query = '';
            if (this.idFieldName) {
                const hidden = this.$el.querySelector(`input[name="${this.idFieldName}"]`);
                if (hidden) hidden.value = '';
            }
        }
    }));
});
