import { ArcElement, BarElement, BubbleController, CategoryScale, Chart as ChartJS, Filler, Legend, LinearScale, LineElement, PointElement, RadialLinearScale, Title, Tooltip } from 'chart.js'

ChartJS.register(
  ArcElement,
  BarElement,
  BubbleController,
  CategoryScale,
  LinearScale,
  RadialLinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
)

export const dashboardTickColor = 'rgba(255, 255, 255, 0.5)'
export const dashboardGridColor = 'rgba(54, 137, 134, 0.15)'
