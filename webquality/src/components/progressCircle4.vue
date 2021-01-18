<template>
    <div class="container is-current" style="backgroundColor:#fff;">
        <div class="fsz14px" style="marginBottom:5px;">{{toptitle}}</div>
        <div style="overflow:hidden;">
            <div class="box" style="height:160px;backgroundColor:#fff;" id="box8"></div>
            <div class="txtp">
                <span class="txt1">{{startvalue}}</span>
                <span class="txt2">/</span>
                <span class="txt3">{{stopvalue}}</span>
                <span class="txt4">项</span>
            </div>
        </div>
    </div>
</template>
<script>
import echarts from '@/assets/js/echarts.js'
export default {
    data(){
            return {
                myecharts4:null
            }
    },
    props:['toptitle','comment','startvalue','stopvalue'],
    mounted(){
        this.drawpic(this.comment,this.startvalue,this.stopvalue)
    },
     beforeDestroy(){
            this.myecharts4.clear()
            this.myecharts4.dispose()
            this.myecharts4=null
      },
    methods: {
         drawpic(comment,startvalue,stopvalue) {
               this.myecharts4=echarts.init(document.getElementById('box8'))
               var option = {
                    title: [{
                        text:comment,
                        x: 'center',
                        top: '55%',
                        textStyle: {
                            color: '#666',
                            fontSize: 12,
                            fontWeight: '100',
                        }
                    }, {
                        text:((startvalue/stopvalue).toFixed(3))*100+'%',
                        x: 'center',
                        top: '40%',
                        textStyle: {
                            fontSize: '20',
                            color: '#FFFFFF',
                            fontFamily: 'DINAlternate-Bold, DINAlternate',
                            foontWeight: '60',
                        },
                    }],
                    backgroundColor: '#fff',
                    polar: {
                        radius: ['68%', '88%'],
                        center: ['50%', '50%'],
                    },
                    angleAxis: {
                        max: stopvalue,
                        show: false,
                    },
                    radiusAxis: {
                        type: 'category',
                        show: true,
                        axisLabel: {
                            show: false,
                        },
                        axisLine: {
                            show: false,
                        },
                        axisTick: {
                            show: false,
                        },
                    },
                    series: [{
                            name: '',
                            type: 'bar',
                            roundCap: true,
                            barWidth: 80,
                            showBackground: true,
                            backgroundStyle: {
                                color: '#aaa',
                            },
                            data: [startvalue],
                            coordinateSystem: 'polar',

                            itemStyle: {
                                normal: {
                                    color: new echarts.graphic.LinearGradient(0, 1, 0, 0, [{
                                            offset: 0,
                                            color: '#C0C0C0',
                                        },
                                        {
                                            offset: 1,
                                            color: '#00FFFF',
                                        },
                                    ]),
                                },
                            },
                        },
                        {
                            name: '',
                            type: 'pie',
                            startAngle: 40,
                            radius: ['95%'],
                            hoverAnimation: false,
                            center: ['50%', '50%'],
                            itemStyle: {
                                color: 'rgba(66, 66, 66, .1)',
                                borderWidth: 1,
                                borderColor: 'pink',
                            },
                            data: [100],
                        },
                        {
                            name: '',
                            type: 'pie',
                            startAngle: 80,
                            radius: ['60%'],
                            hoverAnimation: false,
                            center: ['50%', '50%'],
                            itemStyle: {
                                color: '#aaa',
                                borderWidth: 1,
                                borderColor: '#fff',
                            },
                            data: [100],
                        }
                    ],

                };
               this.myecharts4.setOption(option)
          }
    },
}
</script>
<style scoped>
     .box{
        float:left;
        width:60%;
    }
    .txtp{
        width: 40%;
        background-color: #fff;
        position: relative;
        left:135px;
        height: 160px;
    }
    .txt1{
        position: absolute;
        top:70px;
        right:42px;
        font-size: 29px;
    }
    .txt2{
        position: absolute;
        top:81px;
        right:34px;
    }
    .txt3{
        position: absolute;
        top:82px;
        right:2px;
        font-size: 17px;
    }
    .txt4{
        position: absolute;
        top:114px;
        right:70px;
        font-size: 12px;
        color: #666;
    }
</style>