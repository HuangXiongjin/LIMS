<template>
    <el-row :gutter="20" class="container" :style="conheight">
        <el-col :span='12' style="height:45%;" class="mgb24"><div class="box" id='box'></div></el-col>
        <el-col :span='12' style="height:45%;" class="mgb24"><div class="box">2</div></el-col>
        <el-col :span='12' style="height:50%;"><div class="box">2</div></el-col>
        <el-col :span='12' style="height:50%;"><div class="box">2</div></el-col>
    </el-row>
</template>
<script>
import echarts from '@/assets/js/echarts.js'
export default {
    data(){

        return {
           msg:'12',
           conheight:{
               height:''
           }
        }
    },
    created(){
        this.getInitHeight()
    },
    mounted(){
        this.drawpic()
    },
    beforeDestroy(){
        if(this.myecharts){
            this.myecharts.clear()
            this.myecharts.dispose()
            this.myecharts=null
        }
    },
     mounted(){
        this.drawpic()
    },
    methods: {
        getInitHeight() {
            this.conheight.height=(window.innerHeight-160)+'px'
        },
         drawpic(){
            if(this.myecharts){
                this.myecharts.clear()
                this.myecharts.dispose()
                this.myecharts=null
            }
            this.myecharts=echarts.init(document.getElementById('box'))
            var option = {
                legend: {},
                tooltip: {},
                dataset: {
                    source: [
                        ['product', '2015', '2016', '2017'],
                        ['Matcha Latte', 43.3, 85.8, 93.7],
                        ['Milk Tea', 83.1, 73.4, 55.1],
                        ['Cheese Cocoa', 86.4, 65.2, 82.5],
                        ['Walnut Brownie', 72.4, 53.9, 39.1]
                    ]
                },
                xAxis: {type: 'category'},
                yAxis: {},
                // Declare several bar series, each will be mapped
                // to a column of dataset.source by default.
                series: [
                    {type: 'bar'},
                    {type: 'bar'},
                    {type: 'bar'}
                ]
            };
            this.myecharts.setOption(option)
        }
    },
}
</script>
<style scoped>
  .box{
      background-color:#ccc;
      height: 100%;
  }
</style>