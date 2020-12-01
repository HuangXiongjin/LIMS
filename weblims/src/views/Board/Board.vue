<template>
    <el-row :gutter='20'>
        <el-col :span='14'>
            <div style="height:300px;backgroundColor:#ccc;" id='box'></div>
        </el-col>
        <el-col :span='8'>5</el-col>
    </el-row>
</template>
<script>
import echarts from '@/assets/js/echarts.js'
export default {
    data(){
        return {
            ma:'12',
            myecharts:null
        }
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
    methods: {
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

</style>>
