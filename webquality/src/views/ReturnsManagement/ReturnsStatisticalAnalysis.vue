<template>
    <el-row :style="conheight" style="overflow:auto;">
            <el-row :gutter="20" class="mgt24" >
                <el-col :span="5">
                    <ProgressPie :toptitle='topTitle' :comment='selfcomment' :startvalue='startvalue' :stopvalue='stopvalue'></ProgressPie>
                </el-col>
                <el-col :span="5">
                    <div class="container">
                        <div class="fsz14px">原料质检量<span style="color:pink;marginLeft:16px;">项</span></div>
                        <div class="mgt24" style="fontSize:40px;height:140px;lineHeight:120px;color:#0A9168;">2356</div>
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
                                <span style="color:#0A9168;fontSize:20px;">86.33</span><span style="color:#0A9168;marginLeft:10px;">%</span>
                            </el-col>
                            <el-col :span='24' class="mgt24">
                                <span style="color:#ccc;">最低:</span><span style="color:pink;marginLeft:10px;">原料B</span>
                            </el-col>
                            <el-col :span='24' class="mgt24">
                                <span style="color:pink;fontSize:20px;">65.33</span><span style="color:pink;marginLeft:10px;">%</span>
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
                                <div style="fontSize:40px;height:160px;lineHeight:160px;color:#0A9168;">78.33</div>
                            </el-col>
                        </el-col>
                        <el-col :span='12'>
                            <el-col :span='24'>
                                <span style="color:#ccc;">最高:</span><span style="color:#0A9168;marginLeft:10px;">产品组</span>
                            </el-col>
                            <el-col :span='24' class="mgt24">
                                <span style="color:#0A9168;fontSize:20px;">86.33</span><span style="color:#0A9168;marginLeft:10px;">%</span>
                            </el-col>
                            <el-col :span='24' class="mgt24">
                                <span style="color:#ccc;">最低:</span><span style="color:pink;marginLeft:10px;">小组C</span>
                            </el-col>
                            <el-col :span='24' class="mgt24">
                                <span style="color:pink;fontSize:20px;">65.33</span><span style="color:pink;marginLeft:10px;">%</span>
                            </el-col>
                        </el-col>
                    </el-row>
                </el-col>
            </el-row>
            <el-row :gutter='20' class="mgt24">
                <el-col :span='10'>
                    <WeekBar></WeekBar>
                </el-col>
                <el-col :span='14'>
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
           selfcomment:'已完成',
           startvalue:41,
           stopvalue:200,
           conheight:{
               height:''
           }

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