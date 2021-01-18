<template>
    <el-row :style="conheight" style="overflow:auto;">
            <el-row :gutter="20" class="mgt24" >
                <el-col :span="5">
                    <ProgressPie :toptitle='topTitle' :comment='selfcomment' :startvalue='startvalue' :stopvalue='stopvalue'></ProgressPie>
                </el-col>
                <el-col :span="5">
                    <div class="container" style="position:relative;">
                        <div class="fsz14px">原料质检量<span style="color:pink;marginLeft:16px;">项</span></div>
                        <div class="mgt24" style="fontSize:40px;height:140px;lineHeight:120px;color:#0A9168;">385</div>
                        <div class="mydateclass">
                            <el-select v-model="alldate">
                                <el-option
                                v-for="item in options"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                                </el-option> 
                            </el-select>
                        </div>
                    </div>
                </el-col>
                <el-col :span="7">
                    <el-row class="container">
                        <el-col :span='12'>
                            <el-col :span='24'>
                                质检合格率<span style="color:pink;marginLeft:18px;">%</span>
                            </el-col>
                            <el-col :span='24'>
                                <div style="fontSize:40px;height:160px;lineHeight:160px;color:#0A9168;">78.33</div>
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
                                原料质检准时率<span style="color:pink;marginLeft:18px;">%</span>
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
                                <span style="color:pink;fontSize:20px;">99.9</span><span style="color:pink;marginLeft:10px;">%</span>
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
           topTitle:"原料质检完成情况",
           listTitle:'原料',
           selfcomment:'已完成',
           startvalue:190,
           stopvalue:200,
           conheight:{
               height:''
           },
           data1: [{name: '物料A',value: 23.4,sum: 30,},{name: '物料A1',value: 16,sum: 20},{name: '物料B',value: 15,sum: 20},
                    {name: '物料C',value: 15,sum: 20},{name: '物料D',value: 96,sum: 100},{name: '物料E',value: 98,sum: 100},
                    {name: '物料F',value: 97,sum: 100}],
           data2: [{name: '物料A',value: 33.4,sum: 40,},{name: '物料A1',value: 17,sum: 20},{name: '物料B',value: 45,sum: 50},
                    {name: '物料C',value: 22,sum: 47},{name: '物料D',value: 66,sum: 100},{name: '物料E',value: 58,sum: 100},
                    {name: '物料F',value: 47,sum: 100}],
           alldate:'周',
           mmdate:['22:18', '22:23', '22:25','22:28','22:30','22:33','22:35','22:40','22:18', '22:23', '22:25','22:28','22:30','22:33','22:35','22:40'],
           data3:[60, 62, 80,80,62, 60, 55, 45,10,15, 30, 45, 55, 30, 15, 10],
           data4:[55, 60, 62, 80,80,62, 60,10,15, 30, 45, 55, 45, 30, 15, 10],
           data5:['原料A', '原料B', '原料C', '原料D', '原料E'],
           data6:[20, 120, 119, 134, 100],
           options:[{ value: '年',label: '年'}, {value: '月',label: '月'},{value: '周',label: '周'}]

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