<template>
    <el-row :gutter="20">
        <el-col :span='5'>
            <el-col class="container">
                <div class="fontWet titl">样本分类</div>
                <div style="marginTop:20px;">
                    <el-tree
                    :data="data"
                    show-checkbox
                    node-key="id"
                    :default-expanded-keys="[2, 3]"
                    :default-checked-keys="[5]"
                    :props="defaultProps">
                    </el-tree>
                </div>
            </el-col>
        </el-col>
        <el-col :span='19'>
            <el-col class="container">
                <div class="fontWet titl">请验单填写</div>
                <div style="marginTop:20px;" class="padd15">
                   <el-col :span='24' class="txtgreencolor fsz20">JC20201212</el-col>
                   <el-col :span='24' class='mgt24'>基础数据</el-col>
                   <el-col :span='24' class='mgt24'>
                       <el-form ref="form" :model="requestform" label-width="80px">
                         <el-row :gutter='40'>
                           <el-col :span='10'>
                            <el-form-item label="样品种类">
                                <el-input v-model="requestform.species"></el-input>
                            </el-form-item>
                           </el-col>
                           <el-col :span='10'>
                            <el-form-item label="请验单号">
                                <el-input v-model="requestform.testNo"></el-input>
                            </el-form-item>
                           </el-col>
                           <el-col :span='10'>
                            <el-form-item label="品名/名称">
                                <el-input v-model="requestform.name"></el-input>
                            </el-form-item>
                           </el-col>
                           <el-col :span='10'>
                            <el-form-item label="来料批号">
                                <el-input v-model="requestform.batchNo"></el-input>
                            </el-form-item>
                           </el-col>
                           <el-col :span='10'>
                            <el-form-item label="供货单位">
                                <el-input v-model="requestform.provider"></el-input>
                            </el-form-item>
                           </el-col>
                           <el-col :span='10'>
                            <el-form-item label="物料编码">
                                <el-input v-model="requestform.sampleNo"></el-input>
                            </el-form-item>
                           </el-col>
                         </el-row>
                       </el-form>
                   </el-col>
                   <el-col :span='24' class='mgt24'>请验项目</el-col>
                   <el-col :span='24' class='mgt24'>
                       <el-form ref="form" :model="projectform" label-width="80px">
                         <el-row :gutter='40'>
                           <el-col :span='10'>
                            <el-form-item label="请验工序" class="PuNo">
                                 <el-select v-model="projectform.currentstep" placeholder="请选择请验工序">
                                    <el-option label="工序一" value="1"></el-option>
                                    <el-option label="工序二" value="2"></el-option>
                                 </el-select>
                            </el-form-item>
                           </el-col>
                           <el-col :span='10'>
                            <el-form-item label="请验部门">
                                <el-input v-model="projectform.administry"></el-input>
                            </el-form-item>
                           </el-col>
                           <el-col :span='10'>
                            <el-form-item label="申请时间">
                                <el-input v-model="projectform.requesttime"></el-input>
                            </el-form-item>
                           </el-col>
                           <el-col :span='10'>
                            <el-form-item label="请验人">
                                <el-input v-model="projectform.requestman"></el-input>
                            </el-form-item>
                           </el-col>
                           <el-col :span='10'>
                            <el-form-item label="备注">
                                <el-input type="textarea" v-model="projectform.descriptions"></el-input>
                            </el-form-item>
                           </el-col>
                         </el-row>
                       </el-form>
                   </el-col>
                   <el-col :span='24'>
                       <div style="float:right;">
                        <el-button type="danger">重置</el-button>
                        <el-button type="success">提交</el-button>
                        <el-button type="info">加急申请</el-button>
                       </div>
                   </el-col>
                </div>
            </el-col>
        </el-col>
    </el-row>
</template>
<script>
export default {
    data(){

        return {
           msg:'12',
           requestform:{species:'',testNo:'',name:'',batchNo:'',provider:'',sampleNo:''},
           projectform:{currentstep:'',administry:'',requesttime:'',requestman:'',descriptions:''},

           data: [{
            id: 1,
            label: '一级 1',
            children: [{
                id: 4,
                label: '二级 1-1',
                children: [{
                id: 9,
                label: '三级 1-1-1'
                }, {
                id: 10,
                label: '三级 1-1-2'
                }]
            }]
            }, {
            id: 2,
            label: '一级 2',
            children: [{
                id: 5,
                label: '二级 2-1'
            }, {
                id: 6,
                label: '二级 2-2'
            }]
            }, {
            id: 3,
            label: '一级 3',
            children: [{
                id: 7,
                label: '二级 3-1'
            }, {
                id: 8,
                label: '二级 3-2'
            }]
            }],
            defaultProps: {
            children: 'children',
            label: 'label'
            }

        }
    }
}
</script>
<style scoped>
    .titl{
        height:46px;
        line-height:46px;
        border-bottom:1px solid #ccc;
    }
</style>