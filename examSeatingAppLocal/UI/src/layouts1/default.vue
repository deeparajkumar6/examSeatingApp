<template>
  <v-app>
    <v-navigation-drawer permanent>
      <v-list>
        <v-list-item-title class="text-h6">
          Menu
        </v-list-item-title>

        <v-list-item
          exact
          router
          to="/classes"
        >
          <v-list-item-icon>
            <v-icon>mdi-school</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Classes</v-list-item-title>
        </v-list-item>

        <v-list-item
          exact
          router
          to="/exam-rooms"
        >
          <v-list-item-icon>
            <v-icon>mdi-door</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Exam Rooms</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar color="primary" dark>
      <v-toolbar-title>College Room Manager</v-toolbar-title>
    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
  <!-- <v-main>
    <router-view />
  </v-main> -->
</template>

<script setup>
//
</script>
