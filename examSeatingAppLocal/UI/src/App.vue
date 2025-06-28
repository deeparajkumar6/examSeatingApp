<template>
  <v-app>
    <!-- Top App Bar -->
    <v-app-bar color="primary" dark>
      <v-app-bar-nav-icon @click="drawer = !drawer" />
      <v-toolbar-title>College Room Manager</v-toolbar-title>
    </v-app-bar>
    <!-- Navigation Drawer -->
    <v-navigation-drawer v-model="drawer">
      <v-list dense nav>
        <v-list-item active-class="active-item" to="/">
          <template #prepend>
            <v-icon color="primary">
              mdi-school
            </v-icon>
          </template>
          <v-list-item-title>Classes</v-list-item-title>
        </v-list-item>

        <v-list-item
          active-class="active-item"
          exact
          router
          to="/exam-rooms"
        >
          <template #prepend>
            <v-icon color="primary">
              mdi-door
            </v-icon>
          </template>
          <v-list-item-title>Exam Rooms</v-list-item-title>
        </v-list-item>

        <v-list-item
          active-class="active-item"
          exact
          router
          to="/schedule"
        >
          <template #prepend>
            <v-icon color="primary">
              mdi-calendar-check
            </v-icon>
          </template>
          <v-list-item-title>Room Schedule</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Main Content -->
    <v-main>
      <v-container>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  data () {
    return {
      drawer: true,
    };
  },
};
</script>

<style scoped>
.active-item {
  background-color: #e3f2fd !important;
  border-radius: 8px;
}
.v-list-item {
  border-radius: 6px;
  margin: 4px 8px;
}
.v-list-item:hover {
  background-color: #f5f5f5;
}
</style>
