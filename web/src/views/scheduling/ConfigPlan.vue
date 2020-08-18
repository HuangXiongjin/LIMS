<template>
  <el-row>
    <el-col :span="24">
      <el-form :model="form">
        <el-form-item label="选择品名">
          <el-select v-model="form.TradeName">
            <el-option v-for="(item,index) in form.TradeNameList" :key="index" :label="item.label" :value="item.label"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div class="platformContainer">
        <el-divider>设置得率</el-divider>
        <el-form :inline="true" :model="form">
          <el-form-item label="成品总重量B">
            <el-input v-model="form.totalWeight"><template slot="append">kg</template></el-input>
          </el-form-item>
          <el-form-item label="取样量C">
            <el-input v-model="form.sampleVolume"><template slot="append">kg</template></el-input>
          </el-form-item>
          <el-form-item label="得率=(B+C)/A">
            <el-input v-model="form.yield"><template slot="append">%</template></el-input>
          </el-form-item>
          <el-form-item label="获取的总投料量A">
            <b>{{ form.inventory }}</b>
          </el-form-item>
        </el-form>
        <el-divider>设置安全库存</el-divider>
        <el-form>
          <el-form-item v-for="(item,index) in form.sliderList" :key="index">
            <el-col :span="4" class="marginTop">{{ item.name }}</el-col>
            <el-col :span="20">
              <el-row>
                <el-col :span="4">剩余库存 {{ item.Surplus }}</el-col>
                <el-col :span="20"><el-slider v-model="item.Surplus" :max="item.max"></el-slider></el-col>
              </el-row>
              <el-row>
                <el-col :span="4">安全库存 {{ item.safety }}</el-col>
                <el-col :span="20"><el-slider v-model="item.safety" :max="item.max"></el-slider></el-col>
              </el-row>
            </el-col>
          </el-form-item>
        </el-form>
        <el-divider>设置每日生产批数</el-divider>
        <el-form :inline="true" :model="form">
          <el-form-item label="批数（批/日）">
            <el-input v-model="form.dailyBatch"></el-input>
          </el-form-item>
          <el-form-item label="重量（kg/批）">
            <el-input v-model="form.eachBatchWeight"></el-input>
          </el-form-item>
        </el-form>
        <el-button type="primary">保存</el-button>
      </div>
    </el-col>
  </el-row>
</template>
<script>
export default {
  data() {
    return {
      form:{
        totalWeight:"",
        sampleVolume:"",
        yield:"",
        inventory:"",
        TradeName:"品名1",
        TradeNameList:[
          {label:"品名1"},
          {label:"品名2"},
          {label:"品名3"},
        ],
        sliderList:[
          {name:"陈皮",Surplus:500,safety:500,max:5000},
          {name:"太子参",Surplus:700,safety:300,max:5000},
        ],
        dailyBatch:"",
        eachBatchWeight:"",
      }
    }
  },
  methods: {

  },
}
</script>
<style scoped>

</style>
