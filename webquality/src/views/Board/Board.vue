<template>
    <el-row style="overflow:auto;" :style="conheight">
            <el-row :gutter="20" class="mgt24">
                <el-col :span="5">
                    <ProgressPie :toptitle='topTitle' :comment='selfcomment' :startvalue='startvalue' :stopvalue='stopvalue'></ProgressPie>
                </el-col>
                <el-col :span="5">
                    <ProgressPie2 :toptitle='topTitle2' :comment='selfcomment' :startvalue='startvalue2' :stopvalue='stopvalue'></ProgressPie2>
                </el-col>
                <el-col :span="5">
                    <ProgressPie3 :toptitle='topTitle3' :comment='selfcomment' :startvalue='startvalue3' :stopvalue='stopvalue'></ProgressPie3>
                </el-col>
                <el-col :span="5">
                    <ProgressPie4 :toptitle='topTitle4' :comment='selfcomment' :startvalue='startvalue4' :stopvalue='stopvalue'></ProgressPie4>
                </el-col>
                <el-col :span='4'>
                        <ComparePie></ComparePie>
                </el-col>
            </el-row>
            <el-row :gutter='20' class="mgt24">
                <el-col :span='5' class="container" style="height:350px;">
                    <el-row>
                        <el-col :span='16' style="height:30px;lineHeight:35px;">累积量</el-col>
                        <el-col :span='8'>
                            <el-select v-model="mydate" placeholder="请选择">
                                <el-option
                                v-for="item in options"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                                </el-option> 
                            </el-select>
                        </el-col>                    
                    </el-row>
                    <el-row class="mgt24">
                        <el-col :span='5' class="fsz14px lightbrown" style="height:20px;lineHeight:26px;">共计</el-col>
                        <el-col :span='15' class="fsz20 lightgreen">23589</el-col>
                        <el-col :span='4' class="fsz14px" style="height:20px;lineHeight:26px;">项</el-col>                    
                    </el-row>
                    <el-row class="mgt24">
                        <el-col :span='5' class="fsz14px lightbrown">其中</el-col>
                        <el-col :span='8' class="fsz14px lightbrown">占比类最高：</el-col>
                        <el-col :span='10' class="fsz14px lightbrown">药品B-过程类</el-col>                    
                    </el-row>
                    <el-row class="mgt24">
                        <el-col :span='5' class="fsz14px white">num</el-col>
                        <el-col :span='8'>3526</el-col>
                        <el-col :span='10' class="fsz14px">43%</el-col>                    
                    </el-row>
                    <el-row class="mgt24">
                        <el-col :span='5' class="fsz14px white">num</el-col>
                        <el-col :span='8' class="fsz14px lightbrown">占比类最高：</el-col>
                        <el-col :span='10' class="fsz14px lightbrown">药品A-产品类</el-col>                    
                    </el-row>
                    <el-row class="mgt24">
                        <el-col :span='5' class="fsz14px white">num</el-col>
                        <el-col :span='8'>529</el-col>
                        <el-col :span='10' class="fsz14px">4.7%</el-col>                    
                    </el-row>
                    <el-row class="mgt24">
                        <el-col :span='5' class="fsz14px lightbrown" style="height:20px;lineHeight:26px;">准时率</el-col>
                        <el-col :span='15' class="fsz20 redde">100</el-col>
                        <el-col :span='4' class="fsz14px" style="height:20px;lineHeight:26px;">%</el-col>                    
                    </el-row>
                </el-col>
                <el-col :span='19'>
                    <StickkBar :xdate='mmdate' :res1='data3' :res2='data4'></StickkBar>
                </el-col>
            </el-row>
            <el-row :gutter='20' class="mgt24">
                <el-col :span='10'>
                    <CompareList :res1='data5' :res2='data6'></CompareList>
                </el-col>
                <el-col :span='14'>
                    <LineChart></LineChart>
                </el-col>
            </el-row>
    </el-row>
</template>
<script>
import ProgressPie from '@/components/progressCircle'
import ProgressPie2 from '@/components/progressCircle2'
import ProgressPie3 from '@/components/progressCircle3'
import ProgressPie4 from '@/components/progressCircle4'
import WeekBar from '@/components/weekbar'
import StickkBar from '@/components/stickbar'
import CompareList from '@/components/comparelist'
import LineChart from '@/components/line'
import ComparePie from '@/components/ComparePie'
var moment=require('moment')
export default {
    data(){

        return {
           mydate:'年',
           topTitle:"原料质检完成情况",
           topTitle2:"过程质检完成情况",
           topTitle3:"成品质检完成情况",
           topTitle4:"退货质检完成情况",
           selfcomment:'已完成',
           startvalue:159,
           startvalue2:190,
           startvalue3:187,
           startvalue4:195,
           stopvalue:200,
           conheight:{
               height:''
           },
            data1: [{name: '物料A',value: 33.4,sum: 40,},{name: '物料A1',value: 16,sum: 20},{name: '物料B',value: 15,sum: 20},
                    {name: '物料C',value: 15,sum: 20},{name: '物料D',value: 96,sum: 100},{name: '物料E',value: 98,sum: 100},
                    {name: '物料F',value: 97,sum: 100}],
           data2: [{name: '物料A',value: 33.4,sum: 40,},{name: '物料A1',value: 17,sum: 20},{name: '物料B',value: 45,sum: 50},
                    {name: '物料C',value: 22,sum: 47},{name: '物料D',value: 66,sum: 100},{name: '物料E',value: 58,sum: 100},
                    {name: '物料F',value: 47,sum: 100}],
           mmdate:['22:18', '22:23', '22:25','22:28','22:30','22:33','22:35','22:40','22:18', '22:23', '22:25','22:28','22:30','22:33','22:35','22:40'],
           data3:[60, 62, 10,30,62, 45, 15, 45,10,15, 30, 45, 74, 30, 25, 19],
           data4:[55, 90, 22, 80,40,72, 40,10,15, 30, 75, 55, 45, 30, 40, 34],
           data5:['原料A', '原料B', '原料C', '原料D', '原料E'],
           data6:[120, 50, 119, 64, 80],
           options:[{ value: '年',label: '年'}, {value: '月',label: '月'},{value: '周',label: '周'}]
        }
    },
    components:{
        ProgressPie,WeekBar,StickkBar,CompareList,LineChart,
        ProgressPie2,ProgressPie3,ProgressPie4,ComparePie
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
       },
      },
}
</script>
<style scoped>
   
</style>