<template>
    <el-row style="overflow:auto;" :style="conheight">
            <el-row :gutter="20" class="mgt24">
                <el-col :span="5">
                    <ProgressPie :toptitle='topTitle' :comment='selfcomment' :startvalue='startvalue' :stopvalue='stopvalue'></ProgressPie>
                </el-col>
                <el-col :span="5">
                    <ProgressPie2 :toptitle='topTitle2' :comment='selfcomment' :startvalue='startvalue' :stopvalue='stopvalue'></ProgressPie2>
                </el-col>
                <el-col :span="5">
                    <ProgressPie3 :toptitle='topTitle3' :comment='selfcomment' :startvalue='startvalue' :stopvalue='stopvalue'></ProgressPie3>
                </el-col>
                <el-col :span="5">
                    <ProgressPie4 :toptitle='topTitle4' :comment='selfcomment' :startvalue='startvalue' :stopvalue='stopvalue'></ProgressPie4>
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
                        <el-col :span='10' class="fsz14px">45.33%</el-col>                    
                    </el-row>
                    <el-row class="mgt24">
                        <el-col :span='5' class="fsz14px white">num</el-col>
                        <el-col :span='8' class="fsz14px lightbrown">占比类最高：</el-col>
                        <el-col :span='10' class="fsz14px lightbrown">药品A-产品类</el-col>                    
                    </el-row>
                    <el-row class="mgt24">
                        <el-col :span='5' class="fsz14px white">num</el-col>
                        <el-col :span='8'>3526</el-col>
                        <el-col :span='10' class="fsz14px">45.33%</el-col>                    
                    </el-row>
                    <el-row class="mgt24">
                        <el-col :span='5' class="fsz14px lightbrown" style="height:20px;lineHeight:26px;">准时率</el-col>
                        <el-col :span='15' class="fsz20 redde">78.33</el-col>
                        <el-col :span='4' class="fsz14px" style="height:20px;lineHeight:26px;">%</el-col>                    
                    </el-row>
                </el-col>
                <el-col :span='19'>
                    <StickkBar></StickkBar>
                </el-col>
            </el-row>
            <el-row :gutter='20' class="mgt24">
                <el-col :span='10'>
                    <CompareList></CompareList>
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
           startvalue:41,
           stopvalue:200,
           conheight:{
               height:''
           },
           options:[{ value: '年',label: '年'}, {value: '月',label: '月'},{value: '日',label: '日'}]
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