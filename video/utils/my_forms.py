from django import forms


class ReleaseForm(forms.Form):
    title = forms.CharField(max_length=32, required=True, error_messages={'required': '电影名不能为空！'})
    actor = forms.CharField(max_length=32, required=True, error_messages={'required': '演员不能为空！'})
    score = forms.FloatField()
    desc = forms.CharField(max_length=128, required=False)


    def clean_score(self):
        score = self.cleaned_data['score']
        # print(score, type(score))
        if not isinstance(score, (float, int)) or score > 10 or score < 0:
            raise forms.ValidationError('评分格式不正确！')
        return score