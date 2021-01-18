<template>
    <el-row :style="conheight" style="overflow:auto;">
            <el-row :gutter="20" class="mgt24" >
                <el-col :span="5">
                    <ProgressPie :toptitle='topTitle' :comment='selfcomment' :startvalue='startvalue' :stopvalue='stopvalue'></ProgressPie>
                </el-col>
                <el-col :span="5">
                    <div class="container">
                        <div class="fsz14px">在制品质检量<span style="color:pink;marginLeft:16px;">项</span></div>
                        <div class="mgt24" style="fontSize:40px;height:140px;lineHeight:120px;color:#0A9168;">478</div>
                    </div>
                </el-col>
                <el-col :span="7">
                    <el-row class="container">
                        <el-col :span='12'>
                            <el-col :span='24'>
                                在制品质检合格率<span style="color:pink;marginLeft:18px;">%</span>
                            </el-col>
                            <el-col :span='24'>
                                <div style="fontSize:40px;height:160px;lineHeight:160px;color:#0A9168;">100</div>
                            </el-col>
                        </el-col>
                        <el-col :span='12'>
                            <el-col :span='24'>
                                <span style="color:#ccc;">最高:</span><span style="color:#0A9168;marginLeft:10px;">原料A</span>
                            </el-col>
                            <el-col :span='24' class="mgt24">
                                <span style="color:#0A9168;fontSize:20px;">100</span><span style="color:#0A9168;marginLeft:10px;">%</span>
                            </el-col>
                            <el-col :span='24' class="mgt24">
                                <span style="color:#ccc;">最低:</span><span style="color:pink;marginLeft:10px;">原料B</span>
                            </el-col>
                            <el-col :span='24' class="mgt24">
                                <span style="color:pink;fontSize:20px;">100</span><span style="color:pink;marginLeft:10px;">%</span>
                            </el-col>
                        </el-col>
                    </el-row>
                </el-col>
                <el-col :span="7">
                     <el-row class="container">
                        <el-col :span='12'>
                            <el-col :span='24'>
                                在制品质检准时率<span style="color:pink;marginLeft:18px;">%</span>
                            </el-col>
                            <el-col :span='24'>
                                <div style="fontSize:40px;height:160px;lineHeight:160px;color:#0A9168;">100</div>
                            </el-col>
                        </el-col>
                        <el-col :span='12'>
                            <el-col :span='24'>
                                <span style="color:#ccc;">最高:</span><span style="color:#0A9168;marginLeft:10px;">产品组</span>
                            </el-col>
                            <el-col :span='24' class="mgt24">
                                <span style="color:#0A9168;fontSize:20px;">100</span><span style="color:#0A9168;marginLeft:10px;">%</span>
                            </el-col>
                            <el-col :span='24' class="mgt24">
                                <span style="color:#ccc;">最低:</span><span style="color:pink;marginLeft:10px;">小组C</span>
                            </el-col>
                            <el-col :span='24' class="mgt24">
                                <span style="color:pink;fontSize:20px;">99.8</span><span style="color:pink;marginLeft:10px;">%</span>
                            </el-col>
                        </el-col>
                    </el-row>
                </el-col>
            </el-row>
            <el-row :gutter='20' class="mgt24">
                <el-col :span='10'>
                    <WeekBar :res1='data1' :res2='data2'></WeekBar>
                </el-col>
                <el-col :span='14'>
                    <StickkBar :xdate='mmdate' :res1='data3' :res2='data4' :res3='listTitle'></StickkBar>
                </el-col>
            </el-row>
            <el-row :gutter='20' class="mgt24">
                <el-col :span='10'>
                    <CompareList :res1='data5' :res2='data6' :res3='listTitle'></CompareList>
                </el-col>
                <el-col :span='14'>
                    <LineChart></LineChart>
                </el-col>
            </el-row>
    </el-row>
</template>
<script>
import ProgressPie from '@/components/progressCircle'
import WeekBar from '@/components/weekbar'
import StickkBar from '@/components/stickbar'
import CompareList from '@/components/comparelist'
import LineChart from '@/components/line'
var moment=require('moment')
export default {
    data(){

        return {
           msg:'12',
           topTitle:"在制品质检完成情况",
           listTitle:'在制品',
           selfcomment:'已完成',
           startvalue:85,
           stopvalue:120,
           conheight:{
               height:''
           },
          data1: [{name: '物料A',value: 25.4,sum: 40,},{name: '物料A1',value: 66,sum: 100},{name: '物料B',value: 58,sum: 70},
                    {name: '物料C',value: 17.6,sum: 20},{name: '物料D',value: 56.5,sum: 100},{name: '物料E',value: 48,sum: 60},
                    {name: '物料F',value: 97,sum: 100}],
           data2: [{name: '物料A',value: 33.4,sum: 50,},{name: '物料A1',value: 34.5,sum: 50},{name: '物料B',value: 45.6,sum: 70},
                    {name: '物料C',value: 21,sum: 40},{name: '物料D',value: 16,sum: 20},{name: '物料E',value: 15,sum: 20},
                    {name: '物料F',value: 47.2,sum: 100}],
           mmdate:['22:18', '22:23', '22:25','22:28','22:30','22:33','22:35','22:40','22:18', '22:23', '22:25','22:28','22:30','22:33','22:35','22:40'],
           data3:[40,55, 30, 45, 55, 60, 62, 40,70,62, 60, 55, 35, 30, 15, 10],
           data4:[60,15, 70, 45, 55, 60, 62, 80,50,62, 60, 70, 45, 30, 45, 10],
           data5:['原料A', '原料B', '原料C', '原料D', '原料E'],
           data6:[80, 112, 13, 54, 110],

        }
    },
    components:{
        ProgressPie,WeekBar,StickkBar,CompareList,LineChart
    },
    created(){
         window.addEventListener('resize', this.getHeight);
         this.getHeight()
    },
    mounted(){

    },
    methods: {
        getHeight(){
          this.conheight.height=(window.innerHeight-160)+'px'
       }
      },
}
</script>
<style scoped>
   
</style>