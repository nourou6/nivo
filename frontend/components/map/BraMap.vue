<template>
  <div>
    <ol-overlay
      v-for="feature in SELECTED_MASSIF_HOVER"
      :id="'popup-massif-hover' + feature.get('id')"
      :key="feature.id"
      class="massifHover"
      :position="feature"
    >
      <b-card no-body class="overflow-hidden" bg-variant="light">
        <b-row no-gutters>
          <b-card-body>
            <b-card-title class="captialize-text">
              {{ feature.get('name').toLowerCase() }}
            </b-card-title>
            <b-card-text>
              Dernier Bra:
              {{ formatDateStr(feature.get('latest_record').date) }}
            </b-card-text>
          </b-card-body>
        </b-row>
        <b-row no-gutters>
          <b-col>
            <input-orientation
              :value="feature.get('latest_record').dangerous_slopes"
            />
          </b-col>
          <b-col>
            <div class="bra-risk-indicator">
              <bra-indicator-svg
                :risk="feature.get('latest_record').max_risk"
                :risk-high="feature.get('riskHigh')"
                :risk-low="feature.get('riskLow')"
                :altitude-thresold="feature.get('threshold')"
              />
            </div>
          </b-col>
        </b-row>
        <b-row no-gutters>
          <b-card-body>
            <b-button :to="feature.get('name').toLowerCase()">
              Voir le BRA
            </b-button>
          </b-card-body>
        </b-row>
      </b-card>
    </ol-overlay>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import moment from 'moment'
import InputOrientation from '../utils/InputOrientation'
import OlOverlay from './OlOverlay'
import { mapGettersTypes } from '~/modules/stateTypes'
import BraIndicatorSvg from '~/components/utils/BraIndicatorSvg'

export default {
  components: {
    BraIndicatorSvg,
    OlOverlay,
    InputOrientation,
  },
  computed: {
    ...mapState('map', ['massifs']),
    ...mapGetters('map', [
      mapGettersTypes.SELECTED_MASSIF_CLICK,
      mapGettersTypes.SELECTED_MASSIF_HOVER,
    ]),
  },
  methods: {
    formatDateStr(dateStr) {
      return moment(new Date(dateStr)).format('DD/MM/YYYY')
    },
  },
}
</script>

<style>
.captialize-text {
  text-transform: capitalize;
}
.bra-risk-indicator {
  position: relative;
  margin-left: -30px;
  margin-top: -20px;
}
</style>
