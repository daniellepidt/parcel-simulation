<script>
import { Bar } from 'vue-chartjs'

// const { reactiveProp } = mixins


export default {
  extends: Bar,
  // mixins: [reactiveProp],
  props: {
    labels: {
      type: Array,
      required: true
    },
    data: {
      type: Array,
      required: true
    },
    scales: {
      type: Object,
      required: true
    }
  },
  mounted () {
    this.renderChart(
      {
        labels: this.labels,
        datasets: this.data,
      },
      {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          xAxes: [
            {
              scaleLabel: {
                display: true,
                  labelString: this.scales.x
              }
            }
          ],
          yAxes: [
            {
              scaleLabel: {
                display: true,
                  labelString: this.scales.y
              }
            }
          ]
        }
      }
    )
  }
}
</script>