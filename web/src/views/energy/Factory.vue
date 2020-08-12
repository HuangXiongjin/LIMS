<template>
<div style="height:1380px;">
        <el-row  :gutter="20">
            <el-col :span="17" style="height:700px;">
                <div class="marginBottom-10 text-size-18 font_Weight">
                能耗看板
                </div>
                <div style="height:36px;">
                    <ul><li v-for="(item,index) in toptab" :key="index" @click="ChooseToptap(item)" v-bind:class="{active:item===currentkindModel}" class="floatLeft" style="width:100px;">{{item}}</li></ul>
                </div>
                <div style="marginBottom:15px;height:200px;">
                    <div class="scheduleContainer floatLeft" style="height:200px;width:49%;">
                        <div class="text-size-18 font_Weight">本月耗电成本统计</div>
                        <el-row style="height:40px;lineHeight:40px;">
                            <el-col :span='8' :offset="16" class="text-size-16">RMB 1255421</el-col>
                        </el-row>
                        <el-row style="height:40px;lineHeight:40px;">
                            <el-col :span="6"><div class="brown">月耗电总量</div></el-col>
                            <el-col :span="12"><div class="color-orange">12256</div></el-col>
                            <el-col :span="6"><div class="color-success">9.35%</div></el-col>
                        </el-row>
                        <el-row style="height:40px;lineHeight:40px;">
                            <el-col :span="6"><div class="brown">完成批次量</div></el-col>
                            <el-col :span="6"><div class="active">13</div></el-col>
                            <el-col :span="12"><div class=""><el-progress :text-inside="true" :stroke-width="22" :percentage="70"></el-progress></div></el-col>
                        </el-row>
                        <el-row style="height:40px;lineHeight:40px;">
                            <el-col :span="6"><div class="brown">计划完成率</div></el-col>
                            <el-col :span="6"><div class="color-darkblue">69.36%</div></el-col>
                            <el-col :span="6"><div class="">69.36%</div></el-col>
                            <el-col :span="6"><div class="">13/21</div></el-col>
                        </el-row>
                    </div>
                    <div class="scheduleContainer floatRight" style="height:200px;width:49%;">
                        <el-row>
                            <el-col :span='7'>
                                <el-row  style="height:40px;lineHeight:40px;"><el-col :span='24' class="font_Weight text-size-18">周耗电对比</el-col></el-row>
                                <el-row  style="height:30px;lineHeight:30px;"><el-col :span='24' class="active">本周耗电总值</el-col></el-row>
                                <el-row  style="height:30px;lineHeight:30px;"><el-col :span='12'>11256</el-col><el-col :span='12' class="color-orange">9.35%</el-col></el-row>
                                <el-row  style="height:40px;lineHeight:40px;"><el-col :span='12' class="brown">同期值</el-col><el-col :span='12' class="active">9253</el-col></el-row>
                                <el-row  style="height:40px;lineHeight:40px;"><el-col :span='12' class="brown">峰值日</el-col><el-col :span='12' class="color-orange">周一</el-col></el-row>
                            </el-col>
                            <el-col :span='17'>
                               
                            </el-col>
                        </el-row>
                    </div>
                </div>
                <div class="platformContainer" style="height:400px;">
                    <el-row>
                        <el-col :span='6'>
                            <el-row  style="height:40px;lineHeight:40px;"><el-col :span='24' class="font_Weight text-size-18">区域耗电详情</el-col></el-row>
                            <el-row  style="height:40px;lineHeight:40px;"><el-col :span='24' class="active">汉盟新建综合制剂楼</el-col></el-row>
                            <el-row  style="height:40px;lineHeight:40px;"><el-col :span='24' class="font_Weight text-size-18">区域耗电详情</el-col></el-row>
                            <el-row  style="height:40px;lineHeight:40px;"><el-col :span='6' class="brown">年耗电</el-col><el-col :span='6' >21256</el-col><el-col :span='6' class="brown">月耗量</el-col><el-col :span='6'>21256</el-col></el-row>
                            <el-row  style="height:40px;lineHeight:40px;"><el-col :span='6' class="brown">单日量</el-col><el-col :span='6' >1256</el-col><el-col :span='6' class="brown">日均量</el-col><el-col :span='6'>1256</el-col></el-row>
                            <el-row  style="height:40px;lineHeight:40px;"><el-col :span='6' class="brown">变化值</el-col><el-col :span='6' >2.5%</el-col></el-row>
                            <el-row  style="height:40px;lineHeight:40px;"><el-col :span='8' class="brown">当前批次</el-col><el-col :span='16' class="active">JSKGF20200825H</el-col></el-row>
                            <el-row  style="height:40px;lineHeight:40px;"><el-col :span='8' class="brown">生产时长</el-col><el-col :span='16' class="active">03:53:25</el-col></el-row>
                            <el-row  style="height:30px;lineHeight:30px;"><el-col :span='24' class="brown">内容设备在线情况</el-col></el-row>
                            <el-row  style="height:40px;lineHeight:40px;"><el-col :span='24' class="active"><el-progress :text-inside="true" :stroke-width="22" :percentage="70"></el-progress></el-col></el-row>
                        </el-col>
                        <el-col :span='18'></el-col>
                    </el-row>
                </div>
            </el-col>
            <el-col :span="7">
            <div>
                 <div class="marginBottom-10 text-size-18" style="height:59px;">13333</div>
                 <div class="scheduleContainer floatRight marginBottom" style="height:200px;">
                     <el-row>
                         <el-col :span='11'>
                             <el-row style="height:40px;lineHeight:40px;"><el-col class="text-size-18 font_Weight">区域电耗占比</el-col></el-row>
                             <el-row style="height:30px;lineHeight:30px;"><el-col class="active">汉盟新建综合制剂楼</el-col></el-row>
                             <el-row style="height:30px;lineHeight:30px;"><el-col class="font_Weight">11256</el-col></el-row>
                             <el-row style="height:40px;lineHeight:40px;"><el-col class="brown" :span='18'>完成批次量</el-col><el-col class="text-size-18 active"  :span='6'>11</el-col></el-row>
                             <el-row style="height:40px;lineHeight:40px;"><el-col class="brown" :span='18'>完成批次量</el-col><el-col class="text-size-18 color-orange" :span='6'>11</el-col></el-row>
                         </el-col>
                         <el-col :span='13'>环形图</el-col>
                     </el-row>
                 </div>
                 <div style="height:400px;clear:both;" class="scheduleContainer">
                     <el-row style="height:40px;lineHeight:40px;"><el-col class="text-size-18 font_Weight">故障报警</el-col></el-row>
                     <el-row><el-col  :span='7'>报警设备</el-col><el-col :span='10'>正常设备</el-col><el-col :span='7'>离线设备</el-col></el-row>
                     <el-row><el-col>  <el-divider></el-divider></el-col></el-row>
                     <el-row style="height:35px;lineHeight:35px;"><el-col  :span='8' class="text-size-14">新建综合制剂楼</el-col><el-col :span='5' class="text-size-14">电表2</el-col><el-col :span='5' class="text-size-14">152.2</el-col><el-col :span='6' class="text-size-14">2020-08-05</el-col></el-row>
                     <el-row style="height:35px;lineHeight:35px;"><el-col  :span='8' class="text-size-14">新建综合制剂楼</el-col><el-col :span='5' class="text-size-14">电表2</el-col><el-col :span='5' class="text-size-14">152.2</el-col><el-col :span='6' class="text-size-14">2020-08-05</el-col></el-row>
                     <el-row style="height:35px;lineHeight:35px;"><el-col  :span='8' class="text-size-14">新建综合制剂楼</el-col><el-col :span='5' class="text-size-14">电表2</el-col><el-col :span='5' class="text-size-14">152.2</el-col><el-col :span='6' class="text-size-14">2020-08-05</el-col></el-row>
                     <el-row style="height:35px;lineHeight:35px;"><el-col  :span='8' class="text-size-14">新建综合制剂楼</el-col><el-col :span='5' class="text-size-14">电表2</el-col><el-col :span='5' class="text-size-14">152.2</el-col><el-col :span='6' class="text-size-14">2020-08-05</el-col></el-row>
                 </div>
            </div>
            </el-col>
    </el-row>
    <el-row style="height:200px;" :gutter="20" class="marginBottom">
            <el-col :span="8">
                <div class="scheduleContainer" style="height:200px;">
                    <el-row>
                         <el-col :span='7'>
                             <el-row style="height:40px;lineHeight:40px;"><el-col class="text-size-16 font_Weight">批次完成时间</el-col></el-row>
                             <el-row style="height:30px;lineHeight:30px;"><el-col class="active">年数据</el-col></el-row>
                             <el-row style="height:30px;lineHeight:30px;"><el-col class="brown">月数据</el-col></el-row>
                         </el-col>
                         <el-col :span='17'>雷达图</el-col>
                     </el-row>
                </div>
            </el-col>
            <el-col :span="16">
                <div class="scheduleContainer" style="height:200px;">
                     <el-row>
                         <el-col :span='6'>
                             <el-row style="height:40px;lineHeight:40px;"><el-col class="text-size-16 font_Weight">批次完成时间</el-col></el-row>
                             <el-row style="height:30px;lineHeight:30px;"><el-col class="active">年数据</el-col></el-row>
                             <el-row style="height:30px;lineHeight:30px;"><el-col class="brown">月数据</el-col></el-row>
                             <el-row style="height:30px;lineHeight:30px;"><el-col class="brown">实时数据</el-col></el-row>
                             <el-row style="height:30px;lineHeight:30px;"><el-col class="brown" :span='10'>同比变化</el-col><el-col class="active" :span='12'>-0.56%</el-col></el-row>
                         </el-col>
                         <el-col :span='18'>折线图</el-col>
                     </el-row>
                </div>
            </el-col>
    </el-row>
    <el-row style="height:400px;" :gutter="20">
            <el-col :span="8">
                <div class="scheduleContainer" style="height:400px;">
                    <el-row style="height:40px;lineHeight:40px;">
                        <el-col class="text-size-18 font_Weight" >本日耗电量</el-col>
                        <el-col class="text-size-20 color-orange">1,255,421</el-col>
                    </el-row>
                </div>
            </el-col>
            <el-col :span="8">
                <div class="scheduleContainer" style="height:400px;">
                 <el-row  style="height:40px;lineHeight:40px;">
                        <el-col class="text-size-18 font_Weight">本日耗电量</el-col>
                         <el-row><el-col class="active" :span='8'>新建综合制剂楼</el-col><el-col :span='12' class="marginTop12"><el-progress :percentage="percentage" :color="customColor"></el-progress></el-col><el-col class="active" :span='4'>55.3%</el-col></el-row>
                         <el-row><el-col class="active" :span='8'>新建综合制剂楼</el-col><el-col :span='12' class="marginTop12"><el-progress :percentage="percentage" :color="customColor"></el-progress></el-col><el-col class="active" :span='4'>55.3%</el-col></el-row>
                         <el-row><el-col class="active" :span='8'>新建综合制剂楼</el-col><el-col :span='12' class="marginTop12"><el-progress :percentage="percentage" :color="customColor"></el-progress></el-col><el-col class="active" :span='4'>55.3%</el-col></el-row>
                         <el-row><el-col class="active" :span='8'>新建综合制剂楼</el-col><el-col :span='12' class="marginTop12"><el-progress :percentage="percentage" :color="customColor"></el-progress></el-col><el-col class="active" :span='4'>55.3%</el-col></el-row>
                         <el-row><el-col class="active" :span='8'>新建综合制剂楼</el-col><el-col :span='12' class="marginTop12"><el-progress :percentage="percentage" :color="customColor"></el-progress></el-col><el-col class="active" :span='4'>55.3%</el-col></el-row>
                         <el-row><el-col class="active" :span='8'>新建综合制剂楼</el-col><el-col :span='12' class="marginTop12"><el-progress :percentage="percentage" :color="customColor"></el-progress></el-col><el-col class="active" :span='4'>55.3%</el-col></el-row>
                         <el-row><el-col class="active" :span='8'>新建综合制剂楼</el-col><el-col :span='12' class="marginTop12"><el-progress :percentage="percentage" :color="customColor"></el-progress></el-col><el-col class="active" :span='4'>55.3%</el-col></el-row>
                         <el-row><el-col class="active" :span='8'>新建综合制剂楼</el-col><el-col :span='12' class="marginTop12"><el-progress :percentage="percentage" :color="customColor"></el-progress></el-col><el-col class="active" :span='4'>55.3%</el-col></el-row>
                 </el-row>
                </div>
            </el-col>
            <el-col :span="8"><div class="scheduleContainer" style="height:400px;">3</div></el-col>
    </el-row>
</div>
</template>
<script>
export default {
    data(){
        return {
            toptab:['电能详情','水能详情','汽能详情'],
            currentkindModel:'电',
            systemActive:'电能详情',
            percentage: 20,
            customColor: '#409eff'
        }
    },
    methods:{
        ChooseToptap(a){
            this.currentkindModel=a
        },
    }
}
</script>
<style scoped>
.active{
    color:#06ACB5;
}
.brown{
    color:#B9B9B9;
}
.font_Weight{
    font-weight: 700;
}
.marginTop12{
    margin-top: 12px;
}
</style>