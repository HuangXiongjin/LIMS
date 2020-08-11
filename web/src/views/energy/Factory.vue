<template>
<div>
        <el-row  :gutter="20">
            <el-col :span="17" style="height:700px;">
                <div class="marginBottom-10 text-size-18" style="fontWeight:700;">
                能耗看板
                </div>
                <div style="height:36px;">
                    <ul><li v-for="(item,index) in toptab" :key="index" @click="ChooseToptap(item)" v-bind:class="{active:item===currentkindModel}" class="floatLeft" style="width:100px;">{{item}}</li></ul>
                </div>
                <div style="marginBottom:15px;height:200px;">
                    <div class="scheduleContainer floatLeft" style="height:200px;width:49%;">
                        <div class="text-size-18" style="fontWeight:700;">本月耗电成本统计</div>
                        <el-row style="height:40px;lineHeight:40px;">
                            <el-col :span='8' :offset="16" class="text-size-16">RMB 1255421</el-col>
                        </el-row>
                        <el-row style="height:40px;lineHeight:40px;">
                            <el-col :span="6"><div class="">月耗电总量</div></el-col>
                            <el-col :span="12"><div class="color-orange">12256</div></el-col>
                            <el-col :span="6"><div class="color-success">9.35%</div></el-col>
                        </el-row>
                        <el-row style="height:40px;lineHeight:40px;">
                            <el-col :span="6"><div class="">完成批次量</div></el-col>
                            <el-col :span="6"><div class="color-lightgreen">13</div></el-col>
                            <el-col :span="12"><div class="">----------------------</div></el-col>
                        </el-row>
                        <el-row style="height:40px;lineHeight:40px;">
                            <el-col :span="6"><div class="">计划完成率</div></el-col>
                            <el-col :span="6"><div class="color-darkblue">69.36%</div></el-col>
                            <el-col :span="6"><div class="">69.36%</div></el-col>
                            <el-col :span="6"><div class="">13/21</div></el-col>
                        </el-row>
                    </div>
                    <div class="scheduleContainer floatRight" style="height:200px;width:49%;">
                        <el-row>
                            <el-col :span='6'>
                                <el-row  style="height:40px;lineHeight:40px;"><el-col :span='24'>周耗电对比</el-col></el-row>
                                <el-row  style="height:30px;lineHeight:30px;"><el-col :span='24' class="active">本周耗电总值</el-col></el-row>
                                <el-row  style="height:30px;lineHeight:30px;"><el-col :span='12'>11256</el-col><el-col :span='12' class="color-orange">9.35%</el-col></el-row>
                                <el-row  style="height:40px;lineHeight:40px;"><el-col :span='12'>同期值</el-col><el-col :span='12' class="active">9253</el-col></el-row>
                                <el-row  style="height:40px;lineHeight:40px;"><el-col :span='12'>峰值日</el-col><el-col :span='12' class="color-orange">周一</el-col></el-row>
                            </el-col>
                            <el-col :span='18'>右</el-col>
                        </el-row>
                    </div>
                </div>
                <div class="platformContainer" style="height:400px;">散点图</div>
            </el-col>
            <el-col :span="7">
            <div>
                 <div class="marginBottom-10 text-size-18" style="height:59px;">13333</div>
                 <div class="scheduleContainer floatRight marginBottom" style="height:200px;">123</div>
                 <div style="height:400px;clear:both;" class="scheduleContainer">看板</div>
            </div>
            </el-col>
    </el-row>
    <el-row style="height:200px;" :gutter="20" class="marginBottom">
            <el-col :span=8><div class="scheduleContainer" style="height:200px;">1</div></el-col>
            <el-col :span="16"><div class="scheduleContainer" style="height:200px;">3</div></el-col>
    </el-row>
    <el-row style="height:400px;" :gutter="20">
            <el-col :span=8><div class="scheduleContainer" style="height:400px;">1</div></el-col>
            <el-col :span="8"><div class="scheduleContainer" style="height:400px;">3</div></el-col>
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
            systemActive:'电能详情'
        }
    },
    methods:{
        ChooseToptap(a){
            this.currentkindModel=a
        }
        
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


</style>