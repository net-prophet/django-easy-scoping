/**
 * Copyright (c) 2017-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

const React = require('react');

const CompLibrary = require('../../core/CompLibrary.js');
const MarkdownBlock = CompLibrary.MarkdownBlock; /* Used to read markdown */
const Container = CompLibrary.Container;
const GridBlock = CompLibrary.GridBlock;

const siteConfig = require(process.cwd() + '/siteConfig.js');

function imgUrl(img) {
  return siteConfig.baseUrl + 'img/' + img;
}

function docUrl(doc, language) {
  return siteConfig.baseUrl + 'docs/' + (language ? language + '/' : '') + doc;
}

function pageUrl(page, language) {
  return siteConfig.baseUrl + (language ? language + '/' : '') + page;
}

class Button extends React.Component {
  render() {
    return (
      <div className="pluginWrapper buttonWrapper">
        <a className="button" href={this.props.href} target={this.props.target}>
          {this.props.children}
        </a>
      </div>
    );
  }
}

Button.defaultProps = {
  target: '_self',
};

const SplashContainer = props => (
  <div className="homeContainer">
    <div className="homeSplashFade">
      <div className="wrapper homeWrapper">{props.children}</div>
    </div>
  </div>
);

const ProjectTitle = props => (
  <h2 className="projectTitle">
    {siteConfig.title}
    <small>{siteConfig.tagline}</small>
  </h2>
);

const PageHeader = props => (
  <div className="section promoSection">
    <div className="promoRow">
      <div className="pluginRowBlock">{props.children}</div>
    </div>
  </div>
);

class HomeSplash extends React.Component {
  render() {
    let language = this.props.language || '';
    return (
      <SplashContainer>
        <div className="inner">
          <ProjectTitle />
          <PageHeader>
            <div>
                <a href="https://github.com/net-prophet/django-easy-scoping">GitHub</a>
                <a className="github-button"
                    href= "https://github.com/net-prophet/django-easy-scoping"
                    data-icon="octicon-star"
                    data-count-href="/net-prophet/django-easy-scoping/stargazers"
                    data-show-count={true}
                    data-count-aria-label="# stargazers on GitHub"
                    aria-label="Star this project on GitHub">
                    Star
                </a>
            </div>
          </PageHeader>
        </div>
      </SplashContainer>
    );
  }
}

const Block = props => (
  <Container
    padding={['bottom', 'top']}
    id={props.id}
    background={props.background}>
    <GridBlock align="center" contents={props.children} layout={props.layout} />
  </Container>
);

const Scopes_Aggregate = props => (
  <Block layout="fourColumn">
    {[
      {
        content: 'Take complicated querysets and register them as easy to use Scopes.',
        image: imgUrl('NPlogo2.svg'),
        imageAlign: 'top',
        title: 'Scopes',
      },
      {
        content: 'Using the same syntax register complicated aggregates for quick use.',
        image: imgUrl('NPlogo2.svg'),
        imageAlign: 'top',
        title: 'Aggregates',
      },
    ]}
  </Block>
);

class Index extends React.Component {
  render() {
    let language = this.props.language || '';

    return (
      <div>
        <HomeSplash language={language} />
        <div className="mainContainer">
          <Scopes_Aggregate />
        </div>
      </div>
    );
  }
}

module.exports = Index;
