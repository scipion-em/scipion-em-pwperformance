from pwperformance.main import Timer

class Instance(object):

    def method1(cls): pass

    def method2(cls): pass

    def method3(cls): pass

    def method4(cls): pass

    def method5(cls): pass

    def method6(cls): pass

    def method7(cls): pass

    def method8(cls): pass

    def method9(cls): pass

    def method10(cls): pass

    def method11(cls): pass

    def method12(cls): pass

    def method13(cls): pass

    def method14(cls): pass

    def method15(cls): pass

    def method16(cls): pass

    def method17(cls): pass

    def method18(cls): pass

    def method19(cls): pass

    def method20(cls): pass

    def method21(cls): pass

    def method22(cls): pass

    def method23(cls): pass

    def method24(cls): pass

    def method25(cls): pass

    def method26(cls): pass

    def method27(cls): pass

    def method28(cls): pass

    def method29(cls): pass

    def method30(cls): pass

    def method31(cls): pass

    def method32(cls): pass

    def method33(cls): pass

    def method34(cls): pass

    def method35(cls): pass

    def method36(cls): pass

    def method37(cls): pass

    def method38(cls): pass

    def method39(cls): pass

    def method40(cls): pass

    def method41(cls): pass

    def method42(cls): pass

    def method43(cls): pass

    def method44(cls): pass

    def method45(cls): pass

    def method46(cls): pass

    def method47(cls): pass

    def method48(cls): pass

    def method49(cls): pass

    def method50(cls): pass

class Static(object):
    @classmethod
    def method1(cls): pass
    @classmethod
    def method2(cls): pass
    @classmethod
    def method3(cls): pass
    @classmethod
    def method4(cls): pass
    @classmethod
    def method5(cls): pass
    @classmethod
    def method6(cls): pass
    @classmethod
    def method7(cls): pass
    @classmethod
    def method8(cls): pass
    @classmethod
    def method9(cls): pass
    @classmethod
    def method10(cls): pass
    @classmethod
    def method11(cls): pass
    @classmethod
    def method12(cls): pass
    @classmethod
    def method13(cls): pass
    @classmethod
    def method14(cls): pass
    @classmethod
    def method15(cls): pass
    @classmethod
    def method16(cls): pass
    @classmethod
    def method17(cls): pass
    @classmethod
    def method18(cls): pass
    @classmethod
    def method19(cls): pass
    @classmethod
    def method20(cls): pass
    @classmethod
    def method21(cls): pass
    @classmethod
    def method22(cls): pass
    @classmethod
    def method23(cls): pass
    @classmethod
    def method24(cls): pass
    @classmethod
    def method25(cls): pass
    @classmethod
    def method26(cls): pass
    @classmethod
    def method27(cls): pass
    @classmethod
    def method28(cls): pass
    @classmethod
    def method29(cls): pass
    @classmethod
    def method30(cls): pass
    @classmethod
    def method31(cls): pass
    @classmethod
    def method32(cls): pass
    @classmethod
    def method33(cls): pass
    @classmethod
    def method34(cls): pass
    @classmethod
    def method35(cls): pass
    @classmethod
    def method36(cls): pass
    @classmethod
    def method37(cls): pass
    @classmethod
    def method38(cls): pass
    @classmethod
    def method39(cls): pass
    @classmethod
    def method40(cls): pass
    @classmethod
    def method41(cls): pass
    @classmethod
    def method42(cls): pass
    @classmethod
    def method43(cls): pass
    @classmethod
    def method44(cls): pass
    @classmethod
    def method45(cls): pass
    @classmethod
    def method46(cls): pass
    @classmethod
    def method47(cls): pass
    @classmethod
    def method48(cls): pass
    @classmethod
    def method49(cls): pass
    @classmethod
    def method50(cls): pass



with Timer(msg="Inst.") as t:
    for i in range(1**6):
        Instance()


with Timer(msg="Static") as t:
    for i in range(1**6):
        Static()