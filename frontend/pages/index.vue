<template>
  <div id="app">
    <b-container fluid>
      <b-row>
        <b-col lg="6" md="12" sm="12">
          <bra-data />
        </b-col>
        <b-col lg="6" md="12" sm="12">
          <b-col>
            <base-map>
              <bra-map />
            </base-map>
          </b-col>
          <div class="w-100"></div>
          <b-col>
            <!--            <nivo-data />-->
          </b-col>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import {
  globalActionsTypes as actionsTypes,
  mapMutationTypes,
} from '~/modules/stateTypes'

import BaseMap from '~/components/map/BaseMap'
import BraMap from '~/components/map/BraMap'
import BraData from '~/components/BraData'

export default {
  components: {
    BaseMap,
    BraData,
    BraMap,
  },
  async asyncData({ store }) {
    await store.dispatch(actionsTypes.FETCH_MASSIFS)
    store.commit('map/' + mapMutationTypes.SET_VISIBILITY, {
      layerName: 'massifs',
      visibility: true,
    })
    store.commit('map/' + mapMutationTypes.SET_VISIBILITY, {
      layerName: 'flowcapt',
      visibility: false,
    })
    store.commit('map/' + mapMutationTypes.SET_VISIBILITY, {
      layerName: 'posteNivo',
      visibility: false,
    })
  },
}
</script>
