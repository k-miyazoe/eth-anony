<template>
    <div>
        <a href="https://eagle4.fu.is.saga-u.ac.jp/question-board-saga/">ホーム</a>
        <!-- <v-breadcrumbs :items="items">
            <template v-slot:divider>
                <v-icon>mdi-forward</v-icon>
            </template>
        </v-breadcrumbs> -->
    </div>
</template>

<script>
export default {
    data: () => ({
        items: [
            {
                text: 'ホーム',
                disabled: false,
                href: '/',
            },
        ],
    }),
}
</script>