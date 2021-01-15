<template>
    <div class="container">
        <div class="fsz14px" style="backgroundColor:#fff;color:#666;textAlign:center;">原料质检数量对比</div>
        <div style="overflow:hidden;">
            <div style="height:300px;backgroundColor:#fff;" id="box3"></div>
        </div>
    </div>
</template>
<script>
import echarts from '@/assets/js/echarts.js'
export default {
    data(){
            return {
                stickbar:null
            }
    },
    mounted(){
        this.drawpic()
    },
     beforeDestroy(){
            this.stickbar.clear()
            this.stickbar.dispose()
            this.stickbar=null
      },
    methods: {
         drawpic() {
               this.stickbar=echarts.init(document.getElementById('box3'))
                var option = {
			color: ["#9bbb59","#0B438B","#4141F1","#F81945","#4bacc6","#F89E19","#000000"],
			title: {
				//text: '多个纵轴的折线图'
			},
			tooltip: { //框浮层内容格式器  提示框组件
				trigger: 'axis',
				formatter: '{b}'+'<br>'+'{a0}:{c0}' + '<br>' + '{a1}:{c1}' + '<br>' + '{a2}:{c2}' + '<br>'+'{a3}:{c3}'+ '<br>'+'{a4}:{c4}' + '<br>'+'{a5}:{c5}' + '<br>'+'{a6}:{c6}'
			},
			legend: {
				x: 'right',
				data: ['纵轴一', '纵轴二', '纵轴三', '纵轴四','纵轴五','纵轴六','纵轴七'],
				textStyle: {
					color: "#fff",
					fontsize: 25
				}
			},
			grid: {
				left: '10%',
				right: '14%',
				bottom: '15%',
				containLabel: true
			},
			dataZoom: [{  //于区域缩放
				type: 'inside',
				start: 0,
				end: 100
			}, {
				start: 0,
				end: 10,
				handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
				handleSize: '80%',
				handleStyle: {
					color: '#fff',
					shadowBlur: 3,
					shadowColor: 'rgba(0, 0, 0, 0.6)',
					shadowOffsetX: 2,
					shadowOffsetY: 2
				}
			}],

			xAxis: {
				type: 'category',
				boundaryGap: true,
                data: [1,2,3,4,5,6],
                triggerEvent: true,
				axisLabel: {
				      interval: 0
				    }
			},
			yAxis: [{
					boundaryGap: [0, '50%'],
					axisLine: {
						lineStyle: {
							color: '#9bbb59'
						}
					},
					type: 'value',
					name: '纵轴一',
					position: 'left',//Y轴在图的坐边
					offset: 120,//坐标轴移动120
					axisLabel: {
						formatter: function(value, index) {
							return value;
						},

						textStyle: {
							color: '#9bbb59'//Y轴的文字颜色
						}
                    },
                    triggerEvent: true,
					splitLine: {
						show: false,
					},
				},
				{
					boundaryGap: [0, '50%'],
					axisLine: {
						lineStyle: {
							color: '#0B438B'
						}
                    },
                    triggerEvent: true,
					splitLine: {
						show: false,
					},
					type: 'value',
					name: '纵轴二',
					position: 'left',
					offset: 60,//
					axisLabel: {
						formatter: function(value, index) {

							return value;
						}
					}
				},
				{
					boundaryGap: [0, '50%'],
					axisLine: {
						lineStyle: {
							color: '#4141F1'
						}
					},
					splitLine: {
						show: false,
					},
					type: 'value',
					name: '纵轴三',
					position: 'left',
					axisLabel: {
						formatter: function(value, index) {
							return value;
						}
					},
					axisTick: {
						inside: 'false',
						length: 10,
					}
				}, {
					boundaryGap: [0, '50%'],
					axisLine: {
						lineStyle: {
							color: '#F81945'
						}
					},
					splitLine: {
						show: false,
					},
					type: 'value',
					name: '纵轴四',
					//offset: 50, //坐标轴移动50
					position: 'right',
					axisLabel: {
						formatter: function(value, index) {

							return value;
						}
					},
					axisTick: {
						inside: 'false',
						length: 10,
					}
				},
				{
					boundaryGap: [0, '50%'],
					axisLine: {
						lineStyle: {
							color: '#4bacc6'
						}
					},
					splitLine: {
						show: false,
					},
					type: 'value',
					name: '纵轴五',
					offset: 60, //坐标轴移动50mm
					position: 'right',
					axisLabel: {
						formatter: function(value, index) {
							return value;
						}
					},
					axisTick: {
						inside: 'false',
						length: 10,
					}
				},
				{
					boundaryGap: [0, '50%'],
					axisLine: {
						lineStyle: {
							color: '#F89E19'
						}
					},
					splitLine: {
						show: false,
					},
					type: 'value',
					name: '纵轴六',
					offset: 120, //坐标轴移动50mm
					position: 'right',
					axisLabel: {
						formatter: function(value, index) {
							return value;
						}
					},
					axisTick: {
						inside: 'false',
						length: 10,
					}
				},
				{
					boundaryGap: [0, '50%'],
					axisLine: {
						lineStyle: {
							color: '#000000'
						}
					},
					splitLine: {
						show: false,
					},
					type: 'value',
					name: '纵轴七',
					offset: 180, //坐标轴移动50mm
					position: 'right',
					axisLabel: {
						formatter: function(value, index) {
							return value;
						}
					},
					axisTick: {
						inside: 'false',
						length: 10,
					}
				},
			],
			series: [{
					name: '纵轴一',
					type: 'line',
                    data: [2,1,2,1,2,1],
					lineStyle: {
						color: "rgba(155, 187, 89, 1)"//折线颜色
					},
					yAxisIndex: 0,
				},
				{
					name: '纵轴二',
					type: 'line',
					data: [7,8,4,2,1,2],
					lineStyle: {
						color: "rgba(11, 67, 139, 1)"
					},
					yAxisIndex: 1,
				},
				{
					name: '纵轴三',
					type: 'line',
					data: [9,5,6,9,7,1],
					lineStyle: {
						color: "rgba(65, 65, 241, 1)"
					},
					yAxisIndex: 2,
				},
				{
					name: '纵轴四',
					type: 'line',
					data: [6,8,4,2,3,7],
					lineStyle: {
						color: "rgba(248, 25, 69, 1)"
					},
					yAxisIndex: 3,
				},
				{
					name: '纵轴五',
					type: 'line',
					data: [9,5,4,1,2,7],
					lineStyle: {
						color: "rgba(75, 172, 198, 1)"
					},
					yAxisIndex: 4,
				},
				{
					name: '纵轴六',
					type: 'line',
					data: [4,7,8,4,5,1],
					lineStyle: {
						color: "rgba(248, 158, 25, 1)"
					},
					yAxisIndex: 5,
				},
				{
					name: '纵轴七',
					type: 'line',
					data: [7,5,4,8,1,2],
					lineStyle: {
						color: "rgba(0, 0, 0, 1)"
					},
					yAxisIndex: 6,
				}
			]
        };
        this.stickbar.on('click',function (params) {
                console.log(params)
        })
        
            this.stickbar.setOption(option)
          }
    },
}
</script>
<style scoped>
    
</style>